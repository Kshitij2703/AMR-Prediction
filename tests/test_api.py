"""
Test script for AMR Prediction API.
Demonstrates how to call the API programmatically.

Usage:
    # Terminal 1: Start API server
    uvicorn api:app --reload
    
    # Terminal 2: Run this test
    python test_api.py
"""

import requests

API_URL = "http://localhost:8000"

# Test patient data
patient = {
    "age": 72,
    "gender": "M",
    "admission_type": "EMERGENCY",
    "hospital_expire_flag": 0,
    "antibiotic": "VANCOMYCIN",
    "organism": "STAPHYLOCOCCUS AUREUS",
    "ab_total": 4,
    "ab_unique": 3,
    "ab_duration_days": 7,
    "lab_bun": 28.5,
    "lab_creatinine": 1.5,
    "lab_glucose": None,
    "lab_hemoglobin": 9.2,
    "lab_platelets": None,
    "lab_potassium": 4.3,
    "lab_sodium": 136,
    "lab_wbc": 14.5,
}

print("Testing AMR Prediction API\n")

# 1. Health check
print("1. Health Check")
r = requests.get(f"{API_URL}/health")
print(f"   {r.json()}\n")

# 2. Get available models
print("2. Available Models")
r = requests.get(f"{API_URL}/models")
print(f"   Models: {r.json()['available_models']}\n")

# 3. Prediction without SHAP
print("3. Prediction (no SHAP)")
r = requests.post(f"{API_URL}/predict", json={
    "patient": patient,
    "model": "xgb",
    "explain": False
})
result = r.json()
print(f"   Prediction: {result['prediction']}")
print(f"   Confidence: {result['confidence']}")
print(f"   Probabilities: {result['probabilities']}\n")

# 4. Prediction with SHAP
print("4. Prediction (with SHAP)")
r = requests.post(f"{API_URL}/predict", json={
    "patient": patient,
    "model": "xgb",
    "explain": True
})
result = r.json()
print(f"   Prediction: {result['prediction']}")
if result.get("shap_values"):
    print("   Top 3 SHAP features:")
    shap_sorted = sorted(result["shap_values"].items(), key=lambda x: abs(x[1]), reverse=True)[:3]
    for feat, val in shap_sorted:
        print(f"     {feat}: {val:+.4f}")

print("\n✓ API test complete")
