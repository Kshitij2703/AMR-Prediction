"""
Quick test script to verify AMR predictor works with new features.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.models.amr_predictor import AMRPredictor
from src.models.mappings import get_antibiotic_code, get_organism_code

# Test patient with some missing labs
test_patient = {
    "age": 72,
    "gender_encoded": 1,  # Male
    "adm_enc": "EMERGENCY",
    "HOSPITAL_EXPIRE_FLAG": 0,
    "ab_enc": get_antibiotic_code("VANCOMYCIN"),
    "org_enc": get_organism_code("STAPHYLOCOCCUS AUREUS"),
    "ab_total": 4,
    "ab_unique": 3,
    "ab_duration_days": 7,
    "lab_bun": 28.5,
    "lab_creatinine": 1.5,
    "lab_glucose": None,  # Missing - will be imputed
    "lab_hemoglobin": 9.2,
    "lab_platelets": None,  # Missing - will be imputed
    "lab_potassium": 4.3,
    "lab_sodium": 136,
    "lab_wbc": 14.5,
}

print("Testing AMR Predictor with:")
print(f"  Antibiotic: VANCOMYCIN (code: {test_patient['ab_enc']})")
print(f"  Organism: STAPHYLOCOCCUS AUREUS (code: {test_patient['org_enc']})")
print(f"  Missing labs: glucose, platelets (will be imputed)\n")

predictor = AMRPredictor(model_name="xgb")

# Test without SHAP
print("── Prediction (no SHAP) ──")
result = predictor.predict(test_patient, explain=False)
print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']}")
print(f"Probabilities: {result['probabilities']}\n")

# Test with SHAP
print("── Prediction (with SHAP) ──")
result_shap = predictor.predict(test_patient, explain=True)
print(f"Prediction: {result_shap['prediction']}")
if "shap_values" in result_shap:
    print("Top 5 SHAP features:")
    shap_sorted = sorted(result_shap["shap_values"].items(), key=lambda x: abs(x[1]), reverse=True)[:5]
    for feat, val in shap_sorted:
        print(f"  {feat:20s}: {val:+.4f}")
elif "shap_error" in result_shap:
    print(f"SHAP Error: {result_shap['shap_error']}")

print("\n✓ Test complete")
