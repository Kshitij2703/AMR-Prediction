# AMR Prediction System - Deployment Guide

## Quick Start

### Option 1: Docker Compose (Recommended)
```bash
# Build and start all services
docker-compose up --build

# Access services
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - Web UI: http://localhost:8501
```

### Option 2: Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Terminal 1: Start API
uvicorn api:app --reload

# Terminal 2: Start Web UI
streamlit run web_ui.py
```

---

## System Architecture

```
┌─────────────┐
│   Client    │
│  (Browser)  │
└──────┬──────┘
       │
       ├─────────────────┐
       │                 │
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│  Web UI     │   │  REST API   │
│ (Streamlit) │   │  (FastAPI)  │
│  Port 8501  │   │  Port 8000  │
└─────────────┘   └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │  ML Models  │
                  │  (.pkl)     │
                  └─────────────┘
```

---

## Services

### 1. REST API (Port 8000)
**Endpoints**:
- `POST /predict` - Run prediction
- `GET /models` - List models
- `GET /antibiotics` - List antibiotics
- `GET /organisms` - List organisms
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics
- `GET /logs` - Prediction logs

**Example**:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "patient": {
      "age": 72,
      "gender": "M",
      "admission_type": "EMERGENCY",
      "antibiotic": "VANCOMYCIN",
      "organism": "STAPHYLOCOCCUS AUREUS",
      "ab_total": 4,
      "ab_unique": 3,
      "ab_duration_days": 7,
      "lab_bun": 28.5,
      "lab_creatinine": 1.5
    },
    "model": "xgb",
    "explain": true
  }'
```

### 2. Web UI (Port 8501)
Interactive Streamlit interface for clinical users.

**Features**:
- Patient data entry form
- Real-time prediction
- SHAP explanation visualization
- Probability charts
- Model performance metrics

---

## Monitoring

### Metrics Endpoint
```bash
curl http://localhost:8000/metrics
```

**Output** (Prometheus format):
```
amr_predictions_total 42
amr_predictions_by_model{model="xgb"} 30
amr_predictions_by_model{model="rf"} 8
amr_predictions_by_model{model="nn"} 4
amr_predictions_by_class{class="Susceptible"} 35
amr_predictions_by_class{class="Intermediate"} 3
amr_predictions_by_class{class="Resistant"} 4
amr_avg_response_time_seconds 0.234
```

### Logs
```bash
curl http://localhost:8000/logs?limit=10
```

Logs stored in `logs/predictions.jsonl`:
```json
{"timestamp": "2026-04-24T22:15:30", "model": "xgb", "antibiotic": "VANCOMYCIN", "organism": "STAPHYLOCOCCUS AUREUS", "prediction": "Susceptible", "confidence": 0.9997, "response_time": 0.234}
```

---

## Production Deployment

### 1. Environment Variables
```bash
# Optional: For chatbot only
export GROQ_API_KEY="your_key"

# Optional: Custom API URL for web UI
export API_URL="http://api:8000"
```

### 2. Docker Production Build
```bash
# Build images
docker-compose build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 3. Health Checks
```bash
# API health
curl http://localhost:8000/health

# Docker health status
docker ps
```

### 4. Scaling
```bash
# Scale API instances
docker-compose up -d --scale api=3
```

---

## Integration with Hospital Systems

### HL7/FHIR Integration
```python
# Example: Fetch patient data from FHIR server
import requests

fhir_url = "https://hospital.example.com/fhir/Patient/123"
patient_data = requests.get(fhir_url).json()

# Transform to AMR API format
amr_request = {
    "patient": {
        "age": patient_data["age"],
        "gender": patient_data["gender"],
        # ... map other fields
    },
    "model": "xgb",
    "explain": True
}

# Call AMR API
response = requests.post("http://localhost:8000/predict", json=amr_request)
```

### EHR Integration
- Use hospital's existing API gateway
- Implement authentication (OAuth2/JWT)
- Add audit logging
- Comply with HIPAA requirements

---

## Security Considerations

### 1. Authentication
Add API key authentication:
```python
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

@app.post("/predict")
def predict(request: PredictionRequest, api_key: str = Depends(api_key_header)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(401, "Invalid API key")
    # ... rest of code
```

### 2. HTTPS
Use reverse proxy (nginx) with SSL:
```nginx
server {
    listen 443 ssl;
    server_name amr.hospital.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8000;
    }
}
```

### 3. Rate Limiting
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/predict")
@limiter.limit("10/minute")
def predict(request: Request, ...):
    # ... code
```

---

## Troubleshooting

### API not starting
```bash
# Check logs
docker-compose logs api

# Common issues:
# - Port 8000 already in use: Change port in docker-compose.yml
# - Missing .pkl files: Ensure all model files are present
```

### Web UI can't connect to API
```bash
# Check API is running
curl http://localhost:8000/health

# If using Docker, ensure services are on same network
docker network inspect aisde_default
```

### Slow predictions
```bash
# Check metrics
curl http://localhost:8000/metrics | grep response_time

# Solutions:
# - Use XGBoost (fastest)
# - Disable SHAP explanations
# - Add caching
```

---

## Maintenance

### Update Models
```bash
# Replace .pkl files
cp new_model.pkl mimic_amr_xgb_optimized.pkl

# Restart services
docker-compose restart
```

### Backup Logs
```bash
# Backup prediction logs
tar -czf logs_backup_$(date +%Y%m%d).tar.gz logs/

# Rotate logs (keep last 30 days)
find logs/ -name "*.jsonl" -mtime +30 -delete
```

### Monitor Performance
```bash
# Watch metrics in real-time
watch -n 5 'curl -s http://localhost:8000/metrics'

# Export to Prometheus/Grafana for dashboards
```

---

## Support

For issues or questions:
1. Check logs: `docker-compose logs`
2. Review API docs: http://localhost:8000/docs
3. Test with: `python test_api.py`
