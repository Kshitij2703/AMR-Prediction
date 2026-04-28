"""
AMR Predictor - Inference module using pre-trained MIMIC-III models.
Models: XGBoost (best), RandomForest, NeuralNetwork
Labels: 0=Susceptible, 1=Intermediate, 2=Resistant
"""

import os
import json
import numpy as np
import joblib
from pathlib import Path
from .mappings import LAB_MEANS

MODEL_DIR = Path(__file__).parent

FEATURES = [
    "age", "gender_encoded", "adm_enc", "HOSPITAL_EXPIRE_FLAG",
    "ab_enc", "org_enc", "ab_total", "ab_unique", "ab_duration_days",
    "lab_bun", "lab_creatinine", "lab_glucose", "lab_hemoglobin",
    "lab_platelets", "lab_potassium", "lab_sodium", "lab_wbc"
]

LABEL_MAP = {0: "Susceptible", 1: "Intermediate", 2: "Resistant"}


def _load(name):
    return joblib.load(os.path.join(MODEL_DIR, name))


def _load_results():
    try:
        with open(os.path.join(MODEL_DIR, "results.json")) as f:
            data = json.load(f)
        return data.get("results", {})
    except Exception:
        return {
            "XGBoost":      {"Accuracy": 0.8909, "F1_Macro": 0.7180, "Bal_Accuracy": 0.6933, "MCC": 0.7530},
            "RandomForest": {"Accuracy": 0.7660, "F1_Macro": 0.6139, "Bal_Accuracy": 0.7035, "MCC": 0.5479},
            "NeuralNetwork":{"Accuracy": 0.8324, "F1_Macro": 0.5912, "Bal_Accuracy": 0.5758, "MCC": 0.6122},
        }


class AMRPredictor:
    def __init__(self, model_name="xgb"):
        model_map = {
            "xgb": "mimic_amr_xgb_optimized.pkl",
            "rf":  "mimic_amr_rf.pkl",
            "nn":  "mimic_amr_nn.pkl",
        }
        if model_name not in model_map:
            raise ValueError(f"model_name must be one of {list(model_map)}")

        self.model      = _load(model_map[model_name])
        self.scaler     = _load("mimic_scaler.pkl")
        self.le_ab      = _load("le_ab.pkl")
        self.le_org     = _load("le_org.pkl")
        self.le_adm     = _load("le_adm.pkl")
        self.model_name = model_name.upper() if model_name != "nn" else "NeuralNetwork"
        self.shap_explainer = None

    def _encode(self, patient: dict) -> dict:
        """Encode raw string/float codes to LabelEncoder integers."""
        p = dict(patient)

        # adm_enc: raw string like 'EMERGENCY' -> integer
        if isinstance(p.get("adm_enc"), str):
            p["adm_enc"] = int(self.le_adm.transform([p["adm_enc"]])[0])

        # ab_enc: float code like 90012.0 -> LE integer
        if p.get("ab_enc") is not None:
            p["ab_enc"] = int(self.le_ab.transform([str(float(p["ab_enc"]))])[0])

        # org_enc: float code like 80002.0 -> LE integer
        if p.get("org_enc") is not None:
            p["org_enc"] = int(self.le_org.transform([str(float(p["org_enc"]))])[0])

        return p

    def predict(self, patient: dict, explain: bool = False, adjust_threshold: bool = False, 
                susceptible_penalty: float = 0.5, resistant_boost: float = 1.8) -> dict:
        """
        patient: dict with keys matching FEATURES.
                 ab_enc/org_enc should be float codes from mappings.py.
                 adm_enc should be a raw string like 'EMERGENCY'.
        adjust_threshold: Apply class rebalancing to reduce Susceptible bias
        susceptible_penalty: Multiplier for Susceptible probability (default 0.5)
        resistant_boost: Multiplier for Resistant probability (default 1.8)
        """
        patient = self._encode(patient)

        # Build feature vector with mean imputation for missing labs
        x_raw = []
        for feat in FEATURES:
            val = patient.get(feat)
            if val is None and feat in LAB_MEANS:
                val = LAB_MEANS[feat]
            x_raw.append(val if val is not None else 0)

        x = np.array([x_raw], dtype=float)
        x_scaled = self.scaler.transform(x)

        proba = None
        if hasattr(self.model, "predict_proba"):
            proba = self.model.predict_proba(x_scaled)[0].tolist()
            
            # Adjust thresholds to reduce Susceptible bias
            if adjust_threshold:
                # Apply penalties/boosts
                adjusted_proba = [
                    proba[0] * susceptible_penalty,  # Penalize Susceptible
                    proba[1] * 2.0,                   # Boost Intermediate
                    proba[2] * resistant_boost        # Boost Resistant
                ]
                # Renormalize
                total = sum(adjusted_proba)
                proba = [p / total for p in adjusted_proba]
        
        pred = int(np.argmax(proba) if proba else self.model.predict(x_scaled)[0])
        label = LABEL_MAP[pred]

        result = {
            "prediction": label,
            "label_code": pred,
            "probabilities": {LABEL_MAP[i]: round(p, 4) for i, p in enumerate(proba)} if proba else None,
            "confidence": round(max(proba), 4) if proba else None,
            "model": self.model_name,
        }

        if explain:
            try:
                import shap
                if self.shap_explainer is None:
                    try:
                        # Try with model_output='raw' for multi-class XGBoost
                        self.shap_explainer = shap.TreeExplainer(self.model, model_output='raw')
                    except:
                        # Fallback to default
                        self.shap_explainer = shap.TreeExplainer(self.model)
                
                sv = self.shap_explainer.shap_values(x_scaled)
                
                # Handle different SHAP output formats
                if isinstance(sv, list):
                    class_sv = sv[pred][0]
                elif len(sv.shape) == 3:
                    class_sv = sv[0, :, pred]
                else:
                    class_sv = sv[0, :]
                
                result["shap_values"] = {
                    FEATURES[i]: float(np.array(class_sv[i]).item()) 
                    for i in range(len(FEATURES))
                }
                
                ev = self.shap_explainer.expected_value
                if hasattr(ev, '__len__'):
                    result["shap_base_value"] = float(np.array(ev[pred]).item())
                else:
                    result["shap_base_value"] = float(np.array(ev).item())
            except ImportError:
                result["shap_error"] = "shap library not installed"
            except Exception as e:
                # Fallback to feature importances if SHAP fails
                if hasattr(self.model, 'feature_importances_'):
                    importances = self.model.feature_importances_
                    result["shap_values"] = {
                        FEATURES[i]: float(importances[i]) 
                        for i in range(len(FEATURES))
                    }
                    result["shap_note"] = "Using feature importances (SHAP unavailable)"
                else:
                    result["shap_error"] = f"SHAP failed: {str(e)}"

        return result

    @staticmethod
    def model_performance() -> dict:
        return _load_results()
