"""
Test multiple clinical scenarios to verify model predictions vary.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.models.amr_predictor import AMRPredictor
from src.models.mappings import get_antibiotic_code, get_organism_code

predictor = AMRPredictor(model_name="xgb")

# Test cases with expected outcomes
test_cases = [
    {
        "name": "Case 1: VANCOMYCIN vs STAPH AUREUS (should be Susceptible)",
        "antibiotic": "VANCOMYCIN",
        "organism": "STAPHYLOCOCCUS AUREUS",
        "age": 72,
        "ab_total": 4,
    },
    {
        "name": "Case 2: PENICILLIN vs PSEUDOMONAS (should be Resistant)",
        "antibiotic": "PENICILLIN",
        "organism": "PSEUDOMONAS AERUGINOSA",
        "age": 65,
        "ab_total": 8,
    },
    {
        "name": "Case 3: CIPROFLOXACIN vs E. COLI (variable)",
        "antibiotic": "CIPROFLOXACIN",
        "organism": "ESCHERICHIA COLI",
        "age": 55,
        "ab_total": 2,
    },
    {
        "name": "Case 4: MEROPENEM vs ACINETOBACTER (often Resistant in ICU)",
        "antibiotic": "MEROPENEM",
        "organism": "ACINETOBACTER BAUMANNII",
        "age": 70,
        "ab_total": 10,
    },
    {
        "name": "Case 5: AMPICILLIN vs ENTEROCOCCUS FAECIUM (often Resistant)",
        "antibiotic": "AMPICILLIN",
        "organism": "ENTEROCOCCUS FAECIUM",
        "age": 68,
        "ab_total": 6,
    },
]

print("Testing Multiple Clinical Scenarios\n")
print("=" * 70)

for case in test_cases:
    patient = {
        "age": case["age"],
        "gender_encoded": 1,
        "adm_enc": "EMERGENCY",
        "HOSPITAL_EXPIRE_FLAG": 0,
        "ab_enc": get_antibiotic_code(case["antibiotic"]),
        "org_enc": get_organism_code(case["organism"]),
        "ab_total": case["ab_total"],
        "ab_unique": 3,
        "ab_duration_days": 7,
        "lab_bun": 25.0,
        "lab_creatinine": 1.3,
        "lab_glucose": None,
        "lab_hemoglobin": 10.5,
        "lab_platelets": None,
        "lab_potassium": 4.2,
        "lab_sodium": 138,
        "lab_wbc": 12.0,
    }
    
    result = predictor.predict(patient, explain=False)
    
    print(f"\n{case['name']}")
    print(f"  {case['antibiotic']} vs {case['organism']}")
    print(f"  → Prediction: {result['prediction']}")
    print(f"  → Confidence: {result['confidence']:.1%}")
    print(f"  → Probabilities: S={result['probabilities']['Susceptible']:.1%}, "
          f"I={result['probabilities']['Intermediate']:.1%}, "
          f"R={result['probabilities']['Resistant']:.1%}")

print("\n" + "=" * 70)
print("\n✓ Test complete - Check if predictions vary appropriately")
