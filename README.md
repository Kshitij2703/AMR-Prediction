# AMR Prediction System - Production Ready

Autonomous AI System for Antibiotic Resistance Detection using MIMIC-III trained models.

## 📁 Project Structure

```
aisde/
├── src/                          # Source code
│   ├── api/                      # REST API
│   │   └── api.py               # FastAPI endpoints
│   └── models/                   # ML models and utilities
│       ├── amr_predictor.py     # Inference engine
│       ├── mappings.py          # Name→code mappings
│       ├── knowledge_base.py    # RAG knowledge
│       ├── *.pkl                # Trained models
│       └── *.json               # Model metadata
│
├── web/                          # Web interface
│   └── ui/                       # Clinical user interface
│       └── web_ui.py            # Streamlit UI
│
├── docs/                         # Documentation
│   ├── reports/                  # Technical reports
│   └── guides/                   # User guides
│
├── tests/                        # Test files
│   ├── test_predictor.py        # Unit tests
│   └── test_api.py              # Integration tests
│
├── requirements.txt              # Python dependencies
├── start.sh                      # Startup script
└── PROJECT_STATUS_REPORT.txt    # Current status report
```

## 🚀 Quick Start

```bash
# Start the system
./start.sh

# Access:
# - Web UI: http://localhost:8501
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

## 🧪 Testing

```bash
# Test predictor
python tests/test_predictor.py

# Test API (requires API running)
python tests/test_api.py
```

## 📊 Features

- **REST API** - FastAPI with 7 endpoints, monitoring, logging
- **Web UI** - Streamlit interface for clinical users
- **SHAP Explanations** - Explainable AI for predictions
- **Class Rebalancing** - Adjustable penalties to reduce bias
- **Comprehensive Logging** - JSONL audit trail

## 📚 Documentation

- **[Phase II Report](docs/reports/PROJECT_PHASE_II_REPORT.md)** - Complete technical documentation
- **[Deployment Guide](docs/guides/DEPLOYMENT.md)** - Docker setup, security, troubleshooting
- **[User Guide](docs/guides/USER_GUIDE.md)** - Clinical user manual
- **[Summary](docs/reports/PHASE_II_SUMMARY.md)** - Quick reference

## 🎯 Model Performance

### Training Results (MIMIC-III 2001-2012)

| Model | Accuracy | F1-Macro | Balanced Acc | MCC | Grade |
|-------|----------|----------|--------------|-----|-------|
| **XGBoost** | **89.1%** | **71.8%** | **69.3%** | **0.753** | **B+** |
| RandomForest | 76.6% | 61.4% | 70.4% | 0.548 | C+ |
| NeuralNetwork | 83.2% | 59.1% | 57.6% | 0.612 | C+ |

### Real-World Testing (300 combinations)

**Prediction Distribution**:
- Susceptible: 88% (263/300)
- Intermediate: 0% (0/300)
- Resistant: 12% (37/300)

**Clinical Validation**: 62.5% correct on known resistance patterns

### Comparison to Published Research

| Study | Year | Accuracy | Our Model |
|-------|------|----------|-----------|
| Kanjilal et al. | 2018 | 75-85% | **89.1%** ✅ |
| Yang et al. | 2020 | 82-88% | **89.1%** ✅ |
| Feretzakis et al. | 2021 | 78-84% | **89.1%** ✅ |

**Verdict**: Competitive or better than published research

### Strengths ✅
- High overall accuracy (89%)
- Strong MCC (0.75) — real predictive power
- Correct on common patterns (AMPICILLIN/STAPH → Resistant 98%)
- Fast inference (<0.3s)

### Limitations ⚠️
- Class imbalance bias (88% Susceptible predictions)
- Intermediate class never predicted (0%)
- Misses rare resistance (VRE, intrinsic resistance)
- Low balanced accuracy (69% — misses 40% of minority classes)

**See**: `docs/reports/FINAL_RESULTS_REPORT.md` for complete analysis

## 🔧 API Endpoints

- `POST /predict` - Run AMR prediction
- `GET /models` - List available models
- `GET /antibiotics` - List supported antibiotics (30)
- `GET /organisms` - List supported organisms (19)
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics
- `GET /logs` - Prediction logs

## ⚠️ Important Notes

- This is a **clinical decision support tool**, not a replacement for clinical judgment
- Always consult qualified clinicians for medical decisions
- Culture and sensitivity testing remains the gold standard
- System trained on MIMIC-III data (2001-2012)

## 📝 License & Citation

**Authors**: Chintan Shah, Kshitij Navale  
**Course**: AISDE (AI System Design and Engineering)  
**Date**: April 2026

## 🤝 Support

- Technical issues: See [DEPLOYMENT.md](docs/guides/DEPLOYMENT.md)
- Clinical questions: Consult infectious disease team
- Model performance: Report to antibiotic stewardship committee
