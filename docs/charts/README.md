# AMR Prediction System - Charts & Diagrams

All charts for the project report. Generated on April 27, 2026.

## 📊 Chart List

### 1. Model Performance Comparison (`1_model_performance.png`)
- **Type**: Bar chart
- **Shows**: Accuracy, F1-Macro, Balanced Accuracy, MCC for all 3 models
- **Use in**: Model Performance section
- **Key Insight**: XGBoost is the best model (89.09% accuracy)

### 2. Class Distribution (`2_class_distribution.png`)
- **Type**: Pie chart
- **Shows**: Training data distribution (S: 70%, I: 10%, R: 20%)
- **Use in**: Data Analysis section
- **Key Insight**: Explains why model has class imbalance bias

### 3. Prediction Distribution (`3_prediction_distribution.png`)
- **Type**: Pie chart
- **Shows**: Current model predictions (S: 88%, I: 0%, R: 12%)
- **Use in**: Results section
- **Key Insight**: Model over-predicts Susceptible, never predicts Intermediate

### 4. Confusion Matrix (`4_confusion_matrix.png`)
- **Type**: Heatmap
- **Shows**: True vs Predicted classes
- **Use in**: Error Analysis section
- **Key Insight**: Most errors are false Susceptible predictions

### 5. Class Rebalancing Effect (`5_rebalancing_effect.png`)
- **Type**: Grouped bar chart
- **Shows**: Before/After probabilities with rebalancing
- **Use in**: Solution Implementation section
- **Key Insight**: Rebalancing reduces Susceptible bias

### 6. Feature Importance (`6_feature_importance.png`)
- **Type**: Horizontal bar chart
- **Shows**: Top 10 most important features
- **Use in**: Model Interpretability section
- **Key Insight**: Antibiotic and organism codes are most important

### 7. System Architecture (`7_system_architecture.png`)
- **Type**: Flowchart diagram
- **Shows**: User → UI → API → Models → Prediction flow
- **Use in**: System Design section
- **Key Insight**: Simple 3-tier architecture

### 8. Response Time Distribution (`8_response_time.png`)
- **Type**: Histogram
- **Shows**: API response times (mean ~200ms)
- **Use in**: Performance section
- **Key Insight**: Fast predictions (<1 second)

### 9. ROC Curves (`9_roc_curves.png`)
- **Type**: Line chart (multi-class)
- **Shows**: True Positive Rate vs False Positive Rate
- **Use in**: Clinical Validation section
- **Key Insight**: Good discrimination for Susceptible (AUC=0.92)

### 10. Calibration Plot (`10_calibration_plot.png`)
- **Type**: Line chart
- **Shows**: Predicted probability vs actual frequency
- **Use in**: Model Reliability section
- **Key Insight**: Susceptible predictions are well-calibrated

---

## 📝 How to Use in Report

### Essential Charts (Must Include):
1. **Model Performance Comparison** - Shows XGBoost is best
2. **Class Distribution** - Explains bias problem
3. **Confusion Matrix** - Shows error patterns
4. **Rebalancing Effect** - Shows your solution
5. **System Architecture** - Shows how it works

### Supporting Charts (Should Include):
6. **Feature Importance** - Explains predictions
7. **Prediction Distribution** - Shows current behavior
8. **Response Time** - Shows performance

### Advanced Charts (Optional):
9. **ROC Curves** - Clinical validation
10. **Calibration Plot** - Confidence validation

---

## 🎨 Chart Specifications

- **Resolution**: 300 DPI (print quality)
- **Format**: PNG with transparency
- **Style**: Seaborn whitegrid
- **Colors**: 
  - Susceptible: Green (#28a745)
  - Intermediate: Yellow (#ffc107)
  - Resistant: Red (#dc3545)

---

## 🔄 Regenerating Charts

To regenerate all charts:
```bash
python3 generate_charts.py
```

Charts will be saved to `docs/charts/` directory.

---

## 📐 Recommended Placement in Report

**Section 1: Introduction**
- System Architecture diagram

**Section 2: Data & Methods**
- Class Distribution

**Section 3: Model Performance**
- Model Performance Comparison
- Confusion Matrix
- ROC Curves

**Section 4: Results**
- Prediction Distribution
- Feature Importance

**Section 5: Solution (Rebalancing)**
- Rebalancing Effect

**Section 6: Performance**
- Response Time Distribution
- Calibration Plot

---

Generated: April 27, 2026
Total Charts: 10
Total Size: ~2-3 MB
