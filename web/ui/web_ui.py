"""
AMR Prediction Web UI - Streamlit interface for clinical users.
Usage: streamlit run web/ui/web_ui.py
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import os
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from src.models.mappings import list_antibiotics, list_organisms

API_URL = os.environ.get("API_URL", "http://localhost:8000")

st.set_page_config(page_title="AMR Prediction", page_icon="🦠", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 8px;
        border: none;
        font-size: 1.1rem;
    }
    .result-card {
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        margin: 1rem 0;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🦠 AMR Prediction System</h1>
    <p style="font-size: 1.1rem; margin: 0;">AI-Powered Antibiotic Resistance Detection | MIMIC-III Trained Models</p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Model selection
with st.sidebar:
    st.markdown("### ⚙️ Model Configuration")
    
    model = st.selectbox(
        "Select Model",
        ["xgb", "rf", "nn"],
        format_func=lambda x: {"xgb": "🏆 XGBoost (Best)", "rf": "🌲 Random Forest", "nn": "🧠 Neural Network"}[x]
    )
    
    st.markdown("---")
    st.markdown("### 🎯 Prediction Settings")
    
    explain = st.checkbox("📊 Show SHAP Explanation", value=True, help="Display feature importance")
    
    adjust_threshold = st.checkbox(
        "⚖️ Apply Class Rebalancing", 
        value=True,
        help="Reduces bias toward Susceptible predictions"
    )
    
    if adjust_threshold:
        st.info("💡 **Rebalancing Active**: Reduces over-prediction of Susceptible class")
        susceptible_penalty = st.slider("Susceptible Penalty", 0.3, 1.0, 0.5, 0.1, 
                                       help="Lower = more conservative")
        resistant_boost = st.slider("Resistant Boost", 1.0, 3.0, 1.8, 0.1,
                                    help="Higher = more sensitive to resistance")
    else:
        susceptible_penalty = 1.0
        resistant_boost = 1.0
    
    st.markdown("---")
    st.markdown("### 📊 Model Performance")
    
    try:
        r = requests.get(f"{API_URL}/models", timeout=2)
        perf = r.json()["performance"]
        model_key_map = {"xgb": "XGBoost", "rf": "RandomForest", "nn": "NeuralNetwork"}
        
        for m, metrics in perf.items():
            if m == model_key_map.get(model):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Accuracy", f"{metrics['Accuracy']:.1%}")
                    st.metric("F1-Macro", f"{metrics['F1_Macro']:.1%}")
                with col2:
                    st.metric("Balanced Acc", f"{metrics['Bal_Accuracy']:.1%}")
                    st.metric("MCC", f"{metrics['MCC']:.3f}")
    except:
        st.error("⚠️ API not available")
    
    st.markdown("---")
    st.caption("💡 **Tip**: Enable class rebalancing to reduce false Susceptible predictions")

# Main form with tabs
tab1, tab2, tab3 = st.tabs(["👤 Patient Info", "🧪 Lab Values", "📋 Quick Presets"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Demographics")
        age = st.number_input("Age (years)", 0, 120, 65, help="Patient age")
        gender = st.selectbox("Gender", ["M", "F"])
        admission = st.selectbox("Admission Type", ["EMERGENCY", "ELECTIVE", "URGENT", "NEWBORN"])
        expire_flag = st.selectbox("Hospital Outcome", [0, 1], 
                                  format_func=lambda x: "✅ Alive" if x == 0 else "❌ Expired")
    
    with col2:
        st.markdown("#### Infection Details")
        antibiotic = st.selectbox("💊 Antibiotic", list_antibiotics(), 
                                 help="Select antibiotic being tested")
        organism = st.selectbox("🦠 Organism", list_organisms(),
                               help="Select pathogen organism")
        
        st.markdown("#### Treatment History")
        ab_total = st.number_input("Total Antibiotics Given", 0, 50, 3)
        ab_unique = st.number_input("Unique Antibiotics", 0, 20, 2)
        ab_duration = st.number_input("Treatment Duration (days)", 0, 100, 5)

with tab2:
    st.info("💡 Leave fields empty for automatic mean imputation")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Kidney Function")
        lab_bun = st.number_input("BUN (mg/dL)", 0.0, 200.0, value=None, placeholder="Auto")
        lab_creatinine = st.number_input("Creatinine (mg/dL)", 0.0, 20.0, value=None, placeholder="Auto")
    
    with col2:
        st.markdown("#### Blood Chemistry")
        lab_glucose = st.number_input("Glucose (mg/dL)", 0.0, 500.0, value=None, placeholder="Auto")
        lab_potassium = st.number_input("Potassium (mEq/L)", 0.0, 10.0, value=None, placeholder="Auto")
        lab_sodium = st.number_input("Sodium (mEq/L)", 0.0, 200.0, value=None, placeholder="Auto")
    
    with col3:
        st.markdown("#### Hematology")
        lab_hemoglobin = st.number_input("Hemoglobin (g/dL)", 0.0, 25.0, value=None, placeholder="Auto")
        lab_platelets = st.number_input("Platelets (K/uL)", 0.0, 1000.0, value=None, placeholder="Auto")
        lab_wbc = st.number_input("WBC (K/uL)", 0.0, 100.0, value=None, placeholder="Auto")

with tab3:
    st.markdown("#### 🚀 Quick Test Cases")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🟢 Typical Susceptible Case", use_container_width=True):
            st.session_state.preset = "susceptible"
            st.rerun()
    
    with col2:
        if st.button("🔴 High-Risk Resistant Case", use_container_width=True):
            st.session_state.preset = "resistant"
            st.rerun()
    
    st.markdown("---")
    st.caption("**Susceptible**: 65yo, VANCOMYCIN vs STAPH AUREUS")
    st.caption("**Resistant**: 75yo, AMPICILLIN vs STAPH AUREUS (MRSA pattern)")

# Apply presets if selected
if "preset" in st.session_state:
    if st.session_state.preset == "susceptible":
        age, gender, admission = 65, "M", "EMERGENCY"
        antibiotic, organism = "VANCOMYCIN", "STAPHYLOCOCCUS AUREUS"
        ab_total, ab_unique, ab_duration = 3, 2, 5
    elif st.session_state.preset == "resistant":
        age, gender, admission = 75, "M", "EMERGENCY"
        antibiotic, organism = "AMPICILLIN", "STAPHYLOCOCCUS AUREUS"
        ab_total, ab_unique, ab_duration = 8, 5, 14
    del st.session_state.preset

# Predict button
st.markdown("---")
if st.button("🔬 Run Prediction", type="primary", use_container_width=True):
    with st.spinner("🔄 Analyzing patient data..."):
        try:
            patient = {
                "age": age, "gender": gender, "admission_type": admission,
                "hospital_expire_flag": expire_flag,
                "antibiotic": antibiotic, "organism": organism,
                "ab_total": ab_total, "ab_unique": ab_unique, "ab_duration_days": ab_duration,
                "lab_bun": lab_bun, "lab_creatinine": lab_creatinine,
                "lab_glucose": lab_glucose, "lab_hemoglobin": lab_hemoglobin,
                "lab_platelets": lab_platelets, "lab_potassium": lab_potassium,
                "lab_sodium": lab_sodium, "lab_wbc": lab_wbc,
            }
            
            payload = {
                "patient": patient, 
                "model": model, 
                "explain": explain, 
                "adjust_threshold": adjust_threshold
            }
            
            if adjust_threshold:
                payload["susceptible_penalty"] = susceptible_penalty
                payload["resistant_boost"] = resistant_boost
            
            r = requests.post(f"{API_URL}/predict", json=payload, timeout=30)
            result = r.json()
            
            # Display result with color coding
            st.markdown("---")
            prediction = result["prediction"]
            confidence = result["confidence"]
            
            # Color-coded result card
            color_map = {
                "Susceptible": "#28a745",
                "Intermediate": "#ffc107", 
                "Resistant": "#dc3545"
            }
            emoji_map = {
                "Susceptible": "✅",
                "Intermediate": "⚠️",
                "Resistant": "🚨"
            }
            
            st.markdown(f"""
            <div style="background: {color_map[prediction]}; padding: 2rem; border-radius: 10px; text-align: center; color: white;">
                <h1 style="margin: 0; font-size: 3rem;">{emoji_map[prediction]}</h1>
                <h2 style="margin: 0.5rem 0;">{prediction}</h2>
                <p style="font-size: 1.5rem; margin: 0;">Confidence: {confidence:.1%}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Metrics row
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🎯 Prediction", prediction)
            with col2:
                st.metric("📊 Confidence", f"{confidence:.1%}")
            with col3:
                st.metric("🤖 Model", result["model"])
            with col4:
                rebalanced = "Yes" if adjust_threshold else "No"
                st.metric("⚖️ Rebalanced", rebalanced)
            
            # Probabilities chart
            st.markdown("### 📊 Class Probabilities")
            probs = result["probabilities"]
            
            fig = go.Figure(data=[
                go.Bar(
                    x=list(probs.keys()), 
                    y=list(probs.values()),
                    marker_color=[color_map[k] for k in probs.keys()],
                    text=[f"{v:.1%}" for v in probs.values()],
                    textposition='auto',
                )
            ])
            fig.update_layout(
                yaxis_title="Probability", 
                xaxis_title="Class", 
                height=350,
                showlegend=False,
                yaxis=dict(tickformat=".0%")
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # SHAP explanation
            if "shap_values" in result and result["shap_values"] is not None:
                st.markdown("### 🔍 Feature Importance (SHAP)")
                shap_data = sorted(result["shap_values"].items(), key=lambda x: abs(x[1]), reverse=True)[:10]
                df = pd.DataFrame(shap_data, columns=["Feature", "SHAP Value"])
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=df["SHAP Value"], 
                        y=df["Feature"], 
                        orientation='h',
                        marker_color=df["SHAP Value"].apply(lambda x: '#28a745' if x > 0 else '#dc3545'),
                        text=df["SHAP Value"].apply(lambda x: f"{x:+.3f}"),
                        textposition='auto',
                    )
                ])
                fig.update_layout(
                    xaxis_title="SHAP Value (Impact on Prediction)", 
                    yaxis_title="", 
                    height=400,
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.caption("🟢 Positive values push toward predicted class | 🔴 Negative values push away")
            elif "shap_error" in result:
                st.warning(f"⚠️ SHAP explanation unavailable: {result['shap_error']}")
            elif explain:
                st.info("💡 SHAP explanation was requested but not returned by the model")
            
            # Clinical warning
            st.markdown("---")
            st.warning("⚠️ **Clinical Decision Support Tool** - This is NOT a diagnostic tool. Always perform culture and sensitivity testing and consult infectious disease specialists for treatment decisions.")
            
        except Exception as e:
            st.error(f"❌ Prediction failed: {str(e)}")
            st.info("💡 Make sure the API server is running: `uvicorn src.api.api:app --reload`")
