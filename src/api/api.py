"""
AMR Prediction REST API - Production deployment interface.
Matches Phase I Report "real-time API" deployment requirement.

Usage:
    uvicorn api:app --reload
    
Endpoints:
    POST /predict - Run AMR prediction
    GET /models - List available models and performance
    GET /antibiotics - List available antibiotics
    GET /organisms - List available organisms
    GET /health - Health check
    GET /metrics - Prometheus metrics
    GET /logs - Recent prediction logs
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import json
import time
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field
from typing import Optional
from src.models.amr_predictor import AMRPredictor
from src.models.mappings import list_antibiotics, list_organisms, get_antibiotic_code, get_organism_code

app = FastAPI(
    title="AMR Prediction API",
    description="Antibiotic Resistance Detection using MIMIC-III trained models",
    version="1.0.0"
)

# Logging setup
LOG_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "predictions.jsonl"

# Metrics
metrics = {
    "total_predictions": 0,
    "predictions_by_model": {"xgb": 0, "rf": 0, "nn": 0},
    "predictions_by_class": {"Susceptible": 0, "Intermediate": 0, "Resistant": 0},
    "avg_response_time": 0.0,
}

# Request/Response models
class PatientData(BaseModel):
    age: float = Field(..., ge=0, le=120, description="Patient age in years")
    gender: str = Field(..., pattern="^(M|F|Male|Female)$", description="M/F or Male/Female")
    admission_type: str = Field(..., description="EMERGENCY, ELECTIVE, URGENT, or NEWBORN")
    hospital_expire_flag: int = Field(0, ge=0, le=1, description="0=alive, 1=expired")
    antibiotic: str = Field(..., description="Antibiotic name (e.g., VANCOMYCIN)")
    organism: str = Field(..., description="Organism name (e.g., STAPHYLOCOCCUS AUREUS)")
    ab_total: float = Field(..., ge=0, description="Total antibiotics given")
    ab_unique: float = Field(..., ge=0, description="Unique antibiotics")
    ab_duration_days: float = Field(..., ge=0, description="Antibiotic duration in days")
    lab_bun: Optional[float] = Field(None, description="Blood Urea Nitrogen (mg/dL)")
    lab_creatinine: Optional[float] = Field(None, description="Creatinine (mg/dL)")
    lab_glucose: Optional[float] = Field(None, description="Glucose (mg/dL)")
    lab_hemoglobin: Optional[float] = Field(None, description="Hemoglobin (g/dL)")
    lab_platelets: Optional[float] = Field(None, description="Platelets (K/uL)")
    lab_potassium: Optional[float] = Field(None, description="Potassium (mEq/L)")
    lab_sodium: Optional[float] = Field(None, description="Sodium (mEq/L)")
    lab_wbc: Optional[float] = Field(None, description="White Blood Cell count (K/uL)")

class PredictionRequest(BaseModel):
    patient: PatientData
    model: str = Field("xgb", pattern="^(xgb|rf|nn)$", description="Model: xgb, rf, or nn")
    explain: bool = Field(False, description="Generate SHAP explanation")
    adjust_threshold: bool = Field(False, description="Adjust thresholds to reduce Susceptible bias")
    susceptible_penalty: float = Field(0.5, ge=0.1, le=1.0, description="Penalty for Susceptible class")
    resistant_boost: float = Field(1.8, ge=1.0, le=3.0, description="Boost for Resistant class")

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    probabilities: dict
    model: str
    shap_values: Optional[dict] = None
    shap_error: Optional[str] = None

# Global predictor instances (lazy loaded)
_predictors = {}

def get_predictor(model_name: str) -> AMRPredictor:
    if model_name not in _predictors:
        _predictors[model_name] = AMRPredictor(model_name=model_name)
    return _predictors[model_name]

# Endpoints
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "AMR Prediction API", "timestamp": datetime.now().isoformat()}

@app.get("/metrics", response_class=PlainTextResponse)
def get_metrics():
    """Prometheus-style metrics"""
    lines = [
        f"# HELP amr_predictions_total Total number of predictions",
        f"# TYPE amr_predictions_total counter",
        f"amr_predictions_total {metrics['total_predictions']}",
        "",
        f"# HELP amr_predictions_by_model Predictions by model",
        f"# TYPE amr_predictions_by_model counter",
    ]
    for model, count in metrics["predictions_by_model"].items():
        lines.append(f'amr_predictions_by_model{{model="{model}"}} {count}')
    
    lines.extend([
        "",
        f"# HELP amr_predictions_by_class Predictions by class",
        f"# TYPE amr_predictions_by_class counter",
    ])
    for cls, count in metrics["predictions_by_class"].items():
        lines.append(f'amr_predictions_by_class{{class="{cls}"}} {count}')
    
    lines.extend([
        "",
        f"# HELP amr_avg_response_time_seconds Average response time",
        f"# TYPE amr_avg_response_time_seconds gauge",
        f"amr_avg_response_time_seconds {metrics['avg_response_time']}",
    ])
    
    return "\n".join(lines)

@app.get("/logs")
def get_logs(limit: int = 100):
    """Get recent prediction logs"""
    if not LOG_FILE.exists():
        return {"logs": []}
    
    with open(LOG_FILE) as f:
        logs = [json.loads(line) for line in f.readlines()[-limit:]]
    return {"logs": logs, "count": len(logs)}

@app.get("/models")
def get_models():
    return {
        "available_models": ["xgb", "rf", "nn"],
        "default": "xgb",
        "performance": AMRPredictor.model_performance()
    }

@app.get("/antibiotics")
def get_antibiotics():
    return {"antibiotics": list_antibiotics(), "count": len(list_antibiotics())}

@app.get("/organisms")
def get_organisms():
    return {"organisms": list_organisms(), "count": len(list_organisms())}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    """
    Predict antibiotic susceptibility for a patient.
    Returns: Susceptible, Intermediate, or Resistant
    """
    start_time = time.time()
    
    try:
        # Convert request to predictor format
        patient = request.patient
        
        # Validate antibiotic
        ab_code = get_antibiotic_code(patient.antibiotic)
        if ab_code is None:
            raise HTTPException(400, f"Unknown antibiotic: {patient.antibiotic}")
        
        # Validate organism
        org_code = get_organism_code(patient.organism)
        if org_code is None:
            raise HTTPException(400, f"Unknown organism: {patient.organism}")
        
        # Build patient dict
        patient_data = {
            "age": patient.age,
            "gender_encoded": 1 if patient.gender.upper() in ["M", "MALE"] else 0,
            "adm_enc": patient.admission_type.upper(),
            "HOSPITAL_EXPIRE_FLAG": patient.hospital_expire_flag,
            "ab_enc": ab_code,
            "org_enc": org_code,
            "ab_total": patient.ab_total,
            "ab_unique": patient.ab_unique,
            "ab_duration_days": patient.ab_duration_days,
            "lab_bun": patient.lab_bun,
            "lab_creatinine": patient.lab_creatinine,
            "lab_glucose": patient.lab_glucose,
            "lab_hemoglobin": patient.lab_hemoglobin,
            "lab_platelets": patient.lab_platelets,
            "lab_potassium": patient.lab_potassium,
            "lab_sodium": patient.lab_sodium,
            "lab_wbc": patient.lab_wbc,
        }
        
        # Get predictor and run prediction
        predictor = get_predictor(request.model)
        result = predictor.predict(
            patient_data, 
            explain=request.explain, 
            adjust_threshold=request.adjust_threshold,
            susceptible_penalty=request.susceptible_penalty,
            resistant_boost=request.resistant_boost
        )
        
        # Update metrics
        response_time = time.time() - start_time
        metrics["total_predictions"] += 1
        metrics["predictions_by_model"][request.model] += 1
        metrics["predictions_by_class"][result["prediction"]] += 1
        metrics["avg_response_time"] = (
            (metrics["avg_response_time"] * (metrics["total_predictions"] - 1) + response_time) 
            / metrics["total_predictions"]
        )
        
        # Log prediction
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "model": request.model,
            "antibiotic": patient.antibiotic,
            "organism": patient.organism,
            "prediction": result["prediction"],
            "confidence": result["confidence"],
            "response_time": round(response_time, 3),
        }
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        return PredictionResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Prediction error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
