#!/usr/bin/env python3
"""
Generate detailed system architecture diagram
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.lines as mlines

# Set up figure
fig, ax = plt.subplots(figsize=(16, 12))
ax.set_xlim(0, 16)
ax.set_ylim(0, 12)
ax.axis('off')

# Colors
color_ui = '#e3f2fd'
color_api = '#f3e5f5'
color_model = '#e8f5e9'
color_data = '#fff3e0'
color_log = '#fce4ec'

# Title
ax.text(8, 11.5, 'AMR Prediction System Architecture', 
        ha='center', fontsize=20, fontweight='bold')

# ============================================================================
# LAYER 1: USER & PRESENTATION
# ============================================================================
ax.text(8, 10.8, 'PRESENTATION LAYER', ha='center', fontsize=12, 
        fontweight='bold', style='italic', color='#424242')

# User
user_box = FancyBboxPatch((6.5, 10), 3, 0.6, boxstyle="round,pad=0.1",
                          facecolor='#bbdefb', edgecolor='#1976d2', linewidth=2)
ax.add_patch(user_box)
ax.text(8, 10.3, '👤 User (Clinician)', ha='center', va='center', 
        fontsize=11, fontweight='bold')

# Arrow down
arrow1 = FancyArrowPatch((8, 10), (8, 9.2), arrowstyle='->', 
                        mutation_scale=20, linewidth=2, color='#424242')
ax.add_patch(arrow1)

# Streamlit UI
ui_box = FancyBboxPatch((2, 7.8), 12, 1.3, boxstyle="round,pad=0.1",
                        facecolor=color_ui, edgecolor='#1976d2', linewidth=3)
ax.add_patch(ui_box)
ax.text(8, 8.8, 'Streamlit Web UI (Port 8501)', ha='center', 
        fontsize=13, fontweight='bold')
ax.text(8, 8.5, '• Patient Data Entry Forms  • Model Selection  • Rebalancing Controls', 
        ha='center', fontsize=9)
ax.text(8, 8.2, '• Result Visualization  • Feature Importance Display', 
        ha='center', fontsize=9)
ax.text(8, 7.95, 'Tech: Streamlit, Plotly, Pandas', ha='center', 
        fontsize=8, style='italic', color='#666')

# ============================================================================
# LAYER 2: APPLICATION
# ============================================================================
ax.text(8, 7.3, 'APPLICATION LAYER', ha='center', fontsize=12, 
        fontweight='bold', style='italic', color='#424242')

# Arrow down
arrow2 = FancyArrowPatch((8, 7.8), (8, 7), arrowstyle='->', 
                        mutation_scale=20, linewidth=2, color='#424242')
ax.add_patch(arrow2)
ax.text(9, 7.4, 'HTTP POST /predict', fontsize=8, color='#d32f2f', fontweight='bold')

# FastAPI
api_box = FancyBboxPatch((2, 5.5), 12, 1.4, boxstyle="round,pad=0.1",
                         facecolor=color_api, edgecolor='#7b1fa2', linewidth=3)
ax.add_patch(api_box)
ax.text(8, 6.6, 'FastAPI REST API (Port 8000)', ha='center', 
        fontsize=13, fontweight='bold')

# API Endpoints (left side)
endpoints = [
    'POST /predict',
    'GET /models',
    'GET /antibiotics',
    'GET /organisms'
]
for i, endpoint in enumerate(endpoints):
    ax.text(3, 6.2 - i*0.2, f'• {endpoint}', fontsize=8)

# API Features (right side)
features = [
    'GET /health',
    'GET /metrics',
    'GET /logs',
    'Input Validation'
]
for i, feature in enumerate(features):
    ax.text(10, 6.2 - i*0.2, f'• {feature}', fontsize=8)

ax.text(8, 5.65, 'Tech: FastAPI, Uvicorn, Pydantic', ha='center', 
        fontsize=8, style='italic', color='#666')

# ============================================================================
# LAYER 3: MODEL LAYER
# ============================================================================
ax.text(8, 5, 'MODEL LAYER', ha='center', fontsize=12, 
        fontweight='bold', style='italic', color='#424242')

# Arrow down
arrow3 = FancyArrowPatch((8, 5.5), (8, 4.7), arrowstyle='->', 
                        mutation_scale=20, linewidth=2, color='#424242')
ax.add_patch(arrow3)
ax.text(9, 5.1, 'predictor.predict()', fontsize=8, color='#d32f2f', fontweight='bold')

# AMR Predictor
predictor_box = FancyBboxPatch((3, 3.8), 10, 0.8, boxstyle="round,pad=0.1",
                               facecolor='#fff9c4', edgecolor='#f57c00', linewidth=2)
ax.add_patch(predictor_box)
ax.text(8, 4.4, 'AMRPredictor Class', ha='center', fontsize=12, fontweight='bold')
ax.text(8, 4.05, '• Load Models  • Encode Features  • Predict  • Apply Rebalancing  • Extract Importance', 
        ha='center', fontsize=8)

# Three models
models = [
    {'name': 'XGBoost', 'acc': '89.1%', 'size': '63 MB', 'x': 2.5, 'color': '#4caf50'},
    {'name': 'RandomForest', 'acc': '76.6%', 'size': '281 MB', 'x': 6.5, 'color': '#ff9800'},
    {'name': 'Neural Network', 'acc': '83.2%', 'size': '551 KB', 'x': 10.5, 'color': '#2196f3'}
]

for model in models:
    # Arrow from predictor to model
    arrow = FancyArrowPatch((8, 3.8), (model['x'] + 1.5, 3.2), arrowstyle='->', 
                           mutation_scale=15, linewidth=1.5, color='#424242')
    ax.add_patch(arrow)
    
    # Model box
    model_box = FancyBboxPatch((model['x'], 2), 3, 1.1, boxstyle="round,pad=0.1",
                               facecolor=color_model, edgecolor=model['color'], linewidth=2)
    ax.add_patch(model_box)
    ax.text(model['x'] + 1.5, 2.8, model['name'], ha='center', 
            fontsize=11, fontweight='bold')
    ax.text(model['x'] + 1.5, 2.5, f"Accuracy: {model['acc']}", ha='center', fontsize=9)
    ax.text(model['x'] + 1.5, 2.25, f"Size: {model['size']}", ha='center', fontsize=8)
    ax.text(model['x'] + 1.5, 2.05, '17 features', ha='center', fontsize=8, style='italic')

# ============================================================================
# SUPPORTING FILES
# ============================================================================
ax.text(8, 1.5, 'SUPPORTING FILES', ha='center', fontsize=11, 
        fontweight='bold', style='italic', color='#424242')

support_box = FancyBboxPatch((2, 0.3), 12, 1.1, boxstyle="round,pad=0.1",
                             facecolor=color_data, edgecolor='#f57c00', linewidth=2)
ax.add_patch(support_box)

support_files = [
    'mimic_scaler.pkl (StandardScaler)',
    'le_ab.pkl (Antibiotic Encoder)',
    'le_org.pkl (Organism Encoder)',
    'le_adm.pkl (Admission Encoder)',
    'mimic_features.pkl (Feature List)',
    'results.json (Performance Metrics)'
]

for i, file in enumerate(support_files):
    col = i % 3
    row = i // 3
    ax.text(3 + col * 4, 1.1 - row * 0.3, f'• {file}', fontsize=8)

# ============================================================================
# LOGGING & MONITORING (Side panel)
# ============================================================================
log_box = FancyBboxPatch((14.2, 5.5), 1.6, 1.4, boxstyle="round,pad=0.05",
                         facecolor=color_log, edgecolor='#c2185b', linewidth=2)
ax.add_patch(log_box)
ax.text(15, 6.6, 'LOGGING', ha='center', fontsize=9, fontweight='bold')
ax.text(15, 6.3, '📝 predictions', ha='center', fontsize=7)
ax.text(15, 6.05, '.jsonl', ha='center', fontsize=7)
ax.text(15, 5.75, '📊 Metrics', ha='center', fontsize=7)

# Arrow from API to logging
arrow_log = FancyArrowPatch((14, 6.2), (14.2, 6.2), arrowstyle='->', 
                           mutation_scale=15, linewidth=1.5, color='#c2185b',
                           linestyle='dashed')
ax.add_patch(arrow_log)

# ============================================================================
# DATA FLOW ANNOTATIONS
# ============================================================================
# Input annotation
ax.text(0.5, 8.4, 'INPUT:\n• Demographics\n• Labs\n• Infection Info', 
        fontsize=8, bbox=dict(boxstyle='round', facecolor='#e8f5e9', alpha=0.8))

# Output annotation
ax.text(0.5, 6.2, 'OUTPUT:\n• Prediction\n• Confidence\n• Probabilities\n• Importance', 
        fontsize=8, bbox=dict(boxstyle='round', facecolor='#fff3e0', alpha=0.8))

# ============================================================================
# LEGEND
# ============================================================================
legend_elements = [
    mpatches.Patch(facecolor=color_ui, edgecolor='#1976d2', label='Presentation Layer'),
    mpatches.Patch(facecolor=color_api, edgecolor='#7b1fa2', label='Application Layer'),
    mpatches.Patch(facecolor=color_model, edgecolor='#4caf50', label='Model Layer'),
    mpatches.Patch(facecolor=color_data, edgecolor='#f57c00', label='Data Layer'),
    mpatches.Patch(facecolor=color_log, edgecolor='#c2185b', label='Logging'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9, framealpha=0.9)

# Footer
ax.text(8, 0.05, 'AMR Prediction System | 3-Tier Architecture | Local Deployment', 
        ha='center', fontsize=9, style='italic', color='#666')

plt.tight_layout()
plt.savefig('report_materials/system_architecture_diagram.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("✅ System architecture diagram created: report_materials/system_architecture_diagram.png")
