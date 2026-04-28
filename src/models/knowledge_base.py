"""
AMR Knowledge Base - Domain knowledge extracted from Phase I Report.
Used for RAG retrieval to ground chatbot responses in project-specific facts.
"""

# Each entry: {"id": str, "topic": str, "content": str}
KNOWLEDGE_CHUNKS = [
    {
        "id": "project_overview",
        "topic": "Project Overview",
        "content": (
            "This project builds an Autonomous AI System for Antibiotic Resistance Detection "
            "using MIMIC-III ICU data. It predicts antibiotic susceptibility as Susceptible (S), "
            "Intermediate (I), or Resistant (R) — a multi-class classification task. "
            "The system integrates clinical data, lab reports, and ML models to support "
            "real-time clinical decision-making, addressing the 24+ hour delay in traditional culture tests."
        ),
    },
    {
        "id": "dataset",
        "topic": "Dataset - MIMIC-III",
        "content": (
            "Dataset: MIMIC-III (Medical Information Mart for Intensive Care III). "
            "53,423 ICU stays from Beth Israel Deaconess Medical Center, Boston (2001–2012). "
            "55 continuous features (lab measurements, vital signs), 39 categorical features. "
            "External validation: MIMIC-IV (temporal) and Rambam Hospital, Israel (geographic). "
            "HIPAA-compliant, IRB approved, fully anonymized. "
            "Data leakage: DILUTION_VALUE was removed as a leaky feature."
        ),
    },
    {
        "id": "features",
        "topic": "Model Input Features",
        "content": (
            "17 features used for prediction: age, gender_encoded, adm_enc (admission type: "
            "ELECTIVE/EMERGENCY/NEWBORN/URGENT), HOSPITAL_EXPIRE_FLAG, ab_enc (antibiotic code), "
            "org_enc (organism code), ab_total (total antibiotics given), ab_unique (unique antibiotics), "
            "ab_duration_days, lab_bun, lab_creatinine, lab_glucose, lab_hemoglobin, "
            "lab_platelets, lab_potassium, lab_sodium, lab_wbc. "
            "DILUTION_VALUE was removed to prevent data leakage."
        ),
    },
    {
        "id": "model_performance",
        "topic": "Model Performance Results",
        "content": (
            "Three models trained and evaluated: "
            "XGBoost (best overall): Accuracy=89.1%, F1-Macro=71.8%, Balanced Accuracy=69.3%, MCC=0.753. "
            "RandomForest: Accuracy=76.6%, F1-Macro=61.4%, Balanced Accuracy=70.4%, MCC=0.548. "
            "NeuralNetwork (MLP): Accuracy=83.2%, F1-Macro=59.1%, Balanced Accuracy=57.6%, MCC=0.612. "
            "XGBoost best params: n_estimators=600, max_depth=12, learning_rate=0.1, "
            "subsample=0.6, colsample_bytree=0.6, gamma=0.2, reg_lambda=2. "
            "AUROC on MIMIC-III training: 77.3%, MIMIC-IV temporal: 73.2%, Rambam Hospital: 71.1%."
        ),
    },
    {
        "id": "xai_shap",
        "topic": "XAI - SHAP Analysis",
        "content": (
            "SHAP (SHapley Additive exPlanations) used for global and local feature attribution. "
            "Top predictive features by importance rank: "
            "1. Time-series lab measurements (lactate, WBC, creatinine) — highest importance. "
            "2. Vital signs (blood pressure, heart rate, temperature) — high. "
            "3. Prior antibiotic history (previous exposure patterns) — high. "
            "4. Patient demographics (age, gender, BMI) — medium. "
            "5. Comorbidities (diabetes, renal disease) — medium. "
            "SHAP provides both global feature importance charts and local per-patient breakdowns."
        ),
    },

    {
        "id": "clinical_validation",
        "topic": "Clinical Validation & Mortality Correlation",
        "content": (
            "The model's risk score correlates with patient outcomes: "
            "High-risk group: 30% mortality rate. Low-risk group: 16.8% mortality rate. "
            "This validates clinical relevance and supports integration into clinical workflows. "
            "48-hour advance prediction capability enables timely empiric therapy adjustment, "
            "addressing the 20%+ empiric therapy failure rate in current practice."
        ),
    },
    {
        "id": "limitations",
        "topic": "Limitations & Challenges",
        "content": (
            "Key limitations: "
            "1. Model accuracy below 85% threshold — mitigated by ensemble methods and larger datasets. "
            "2. Intermediate (I) category severely underrepresented — addressed with cost-sensitive learning. "
            "3. External validation performance drop (77.3% → 71.1%) — federated learning planned. "
            "4. Explainability vs accuracy trade-off — hybrid models with post-hoc XAI. "
            "5. Geographic bias — models trained on US ICU data may not generalize globally. "
            "6. Temporal validity — resistance patterns evolve, requiring continuous retraining."
        ),
    },
    {
        "id": "future_work",
        "topic": "Future Work",
        "content": (
            "Future research directions: "
            "1. Federated Learning — multi-hospital collaboration without data sharing. "
            "2. National AMR Surveillance Integration — population-level insights. "
            "3. Counterfactual Explanations — 'What if patient had different lab values?' scenarios. "
            "4. Real-time Genomic Integration — rapid sequencing for faster resistance detection. "
            "5. Patient-Facing Explanations — shared decision-making tools with accessible AI explanations."
        ),
    },
    {
        "id": "amr_background",
        "topic": "AMR Background & Clinical Context",
        "content": (
            "Antimicrobial resistance (AMR) is a top-10 global public health threat (WHO). "
            "1.7 million sepsis cases annually in the US; ~350,000 deaths during hospitalization. "
            "Traditional culture-based susceptibility testing takes 24+ hours. "
            "Empiric therapy fails in >20% of cases due to resistance. "
            "Susceptible (S): antibiotic is effective. Intermediate (I): may be effective at higher doses. "
            "Resistant (R): antibiotic is not effective against the pathogen."
        ),
    },
    {
        "id": "system_architecture",
        "topic": "System Architecture",
        "content": (
            "6-stage end-to-end pipeline: "
            "1. Data Collection — lab reports, EHR data, resistance history. "
            "2. Data Engineering — missing values, normalization, feature extraction. "
            "3. Model Development — Random Forest, XGBoost, Neural Networks, Ensemble. "
            "4. System Validation — cross-validation, MIMIC-IV test, Rambam test. "
            "5. Deployment — HIS/LIS integration, real-time API. "
            "6. Monitoring — performance tracking, drift detection."
        ),
    },
]


def get_all_chunks() -> list[dict]:
    return KNOWLEDGE_CHUNKS


def get_chunk_by_topic(topic: str) -> dict | None:
    topic_lower = topic.lower()
    for chunk in KNOWLEDGE_CHUNKS:
        if topic_lower in chunk["topic"].lower() or topic_lower in chunk["content"].lower():
            return chunk
    return None
