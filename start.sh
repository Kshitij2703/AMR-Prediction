#!/bin/bash

echo "🚀 Starting AMR Prediction System..."
echo ""

# Kill existing processes
pkill -f "uvicorn src.api.api:app" 2>/dev/null
pkill -f "streamlit run web/ui/web_ui.py" 2>/dev/null
sleep 2

# Start API
echo "📡 Starting API server..."
python3.10 -m uvicorn src.api.api:app --host 0.0.0.0 --port 8000 > /tmp/api.log 2>&1 &
sleep 3

# Check API
if lsof -ti:8000 > /dev/null 2>&1; then
  echo "   ✅ API running on http://localhost:8000"
  echo "   📖 API docs: http://localhost:8000/docs"
else
  echo "   ❌ API failed to start"
  exit 1
fi

# Start UI
echo ""
echo "🎨 Starting Web UI..."
python3.10 -m streamlit run web/ui/web_ui.py --server.port 8501 --server.headless true > /tmp/streamlit.log 2>&1 &
sleep 4

# Check UI
if lsof -ti:8501 > /dev/null 2>&1; then
  echo "   ✅ UI running on http://localhost:8501"
else
  echo "   ❌ UI failed to start"
  exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "   🌐 Open in browser: http://localhost:8501"
echo ""
echo "   📊 Model Performance:"
echo "      • XGBoost: 89.1% accuracy (Best)"
echo "      • RandomForest: 76.6% accuracy"
echo "      • Neural Network: 83.2% accuracy"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 To stop: pkill -f uvicorn && pkill -f streamlit"
echo ""
