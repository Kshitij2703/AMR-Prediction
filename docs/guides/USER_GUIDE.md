# AMR Prediction System - User Guide

## For Clinical Users

### What is this system?

The AMR (Antimicrobial Resistance) Prediction System helps clinicians predict whether a specific antibiotic will be effective against a bacterial infection **before** traditional culture results are available (which take 24+ hours).

**Key Benefits**:
- ⏱️ **48-hour advance prediction** - Get results before culture tests
- 🎯 **89.1% accuracy** - Trained on 53,000+ ICU cases (MIMIC-III)
- 🔍 **Explainable AI** - See which factors drive each prediction
- 📊 **Confidence scores** - Know how certain the prediction is

---

## How to Use the Web Interface

### Step 1: Access the System
Open your browser and go to: **http://localhost:8501**

### Step 2: Enter Patient Information

#### Demographics
- **Age**: Patient age in years
- **Gender**: M (Male) or F (Female)
- **Admission Type**: 
  - EMERGENCY - Emergency admission
  - ELECTIVE - Scheduled admission
  - URGENT - Urgent but not emergency
  - NEWBORN - Newborn admission

#### Antibiotic & Organism
- **Antibiotic**: Select from 30 common antibiotics (e.g., VANCOMYCIN, MEROPENEM)
- **Organism**: Select from 19 common organisms (e.g., STAPHYLOCOCCUS AUREUS, E. COLI)

#### Antibiotic History
- **Total Antibiotics Given**: How many antibiotic doses total
- **Unique Antibiotics**: How many different antibiotics
- **Duration**: How many days on antibiotics

#### Laboratory Values
Enter available lab values. **You can skip any missing labs** - the system will use statistical imputation.

- **BUN** (Blood Urea Nitrogen): mg/dL
- **Creatinine**: mg/dL
- **Glucose**: mg/dL
- **Hemoglobin**: g/dL
- **Platelets**: K/uL
- **Potassium**: mEq/L
- **Sodium**: mEq/L
- **WBC** (White Blood Cells): K/uL

### Step 3: Configure Prediction

**Model Selection** (sidebar):
- **xgb** (XGBoost) - **Recommended** - Best accuracy (89.1%)
- **rf** (RandomForest) - Good balance (76.6%)
- **nn** (Neural Network) - Alternative (83.2%)

**SHAP Explanation**:
- ✅ Check to see which factors influenced the prediction
- ⬜ Uncheck for faster results

### Step 4: Get Results

Click **"🔬 Predict Susceptibility"**

#### Understanding Results

**Prediction**: One of three outcomes:
- 🟢 **Susceptible** - Antibiotic is likely effective
- 🟡 **Intermediate** - May work at higher doses
- 🔴 **Resistant** - Antibiotic unlikely to work

**Confidence**: How certain the model is (0-100%)
- >90% - Very confident
- 70-90% - Moderately confident
- <70% - Low confidence (use caution)

**Probabilities Chart**: Shows likelihood of each outcome

**SHAP Feature Importance** (if enabled):
- Shows which patient factors most influenced the prediction
- Positive values = pushes toward predicted class
- Negative values = pushes away from predicted class

---

## Clinical Interpretation

### Example 1: High Confidence Susceptible
```
Patient: 72yo male, VANCOMYCIN vs STAPH AUREUS
Prediction: Susceptible (99.7% confidence)
Top SHAP: Antibiotic code (+4.67)
```

**Interpretation**: Very high confidence that VANCOMYCIN will work. The antibiotic choice itself is the strongest predictor (VANCOMYCIN is typically effective against STAPH AUREUS).

**Action**: Proceed with VANCOMYCIN therapy.

### Example 2: Moderate Confidence Resistant
```
Patient: 65yo female, CIPROFLOXACIN vs E. COLI
Prediction: Resistant (75% confidence)
Top SHAP: Prior antibiotic exposure (+2.3)
```

**Interpretation**: Moderate confidence of resistance. Prior antibiotic use suggests possible resistance development.

**Action**: Consider alternative antibiotic. Wait for culture confirmation if possible.

### Example 3: Low Confidence
```
Patient: 45yo male, MEROPENEM vs PSEUDOMONAS
Prediction: Intermediate (55% confidence)
```

**Interpretation**: Model is uncertain. Intermediate category is inherently difficult to predict.

**Action**: Wait for culture results. Consider infectious disease consultation.

---

## Important Warnings

### ⚠️ This is a Decision Support Tool

**NOT a replacement for**:
- Clinical judgment
- Culture and sensitivity testing
- Infectious disease consultation
- Standard of care protocols

**Always**:
- ✅ Consult with qualified clinicians
- ✅ Follow hospital antibiotic stewardship guidelines
- ✅ Order culture tests
- ✅ Monitor patient response
- ✅ Adjust therapy based on culture results

### When to Use This System

**Good use cases**:
- ✅ Empiric therapy selection while waiting for cultures
- ✅ Risk stratification for antibiotic resistance
- ✅ Supporting antibiotic stewardship decisions
- ✅ Educational tool for trainees

**Do NOT use for**:
- ❌ Sole basis for antibiotic selection
- ❌ Overriding culture results
- ❌ Delaying appropriate therapy
- ❌ Patients with unusual infections

---

## Frequently Asked Questions

### Q: How accurate is this system?
**A**: 89.1% accuracy on MIMIC-III test set (XGBoost model). External validation: 73.2% (MIMIC-IV), 71.1% (Rambam Hospital).

### Q: What if I don't have all lab values?
**A**: The system uses mean imputation for missing labs based on training data. However, more complete data gives better predictions.

### Q: Why does it say "Susceptible" but culture shows "Resistant"?
**A**: The model predicts based on statistical patterns, not definitive testing. Culture results are the gold standard. Report discrepancies to your IT team for model improvement.

### Q: Can I use this for rare organisms?
**A**: The system is trained on 19 common organisms. For rare organisms, predictions may be less reliable. Always defer to culture results.

### Q: What does SHAP mean?
**A**: SHAP (SHapley Additive exPlanations) shows which patient factors contributed most to the prediction. Positive values push toward the predicted class, negative values push away.

### Q: How often is the model updated?
**A**: Contact your IT department for model update schedule. Resistance patterns evolve, so regular updates are important.

### Q: Is my patient data stored?
**A**: Predictions are logged for quality monitoring. Check with your institution's privacy policy. No data is sent to external servers.

---

## Troubleshooting

### "API not available" error
**Solution**: Contact IT support. The backend API may be down.

### Prediction takes too long
**Solution**: Disable SHAP explanation for faster results.

### Unknown antibiotic/organism
**Solution**: Check spelling. Only 30 antibiotics and 19 organisms are supported. Use the dropdown menus.

### Results don't make clinical sense
**Solution**: 
1. Verify all inputs are correct
2. Check confidence score (low confidence = uncertain)
3. Consult infectious disease if needed
4. Report issue to IT for investigation

---

## Contact & Support

**Technical Issues**: Contact your hospital IT support  
**Clinical Questions**: Consult infectious disease team  
**Model Performance**: Report to antibiotic stewardship committee

---

## Training Resources

### For New Users
1. Watch demo video (if available)
2. Try test cases with known outcomes
3. Compare predictions with culture results
4. Attend training session

### Test Cases
Use these to familiarize yourself with the system:

**Test 1**: VANCOMYCIN vs STAPH AUREUS (should predict Susceptible)  
**Test 2**: CIPROFLOXACIN vs PSEUDOMONAS (variable, check confidence)  
**Test 3**: MEROPENEM vs ACINETOBACTER (often Resistant in ICU)

---

## Version Information

**System Version**: 1.0.0  
**Model Training Data**: MIMIC-III (2001-2012)  
**Last Updated**: April 2026  
**Models**: XGBoost, RandomForest, NeuralNetwork
