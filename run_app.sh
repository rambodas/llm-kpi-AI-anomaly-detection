#!/bin/bash
echo "🔁 Creating virtual environment..."
python3 -m venv env
source env/bin/activate

echo "⬇️ Installing dependencies..."
pip install -r requirements.txt

echo "🚀 Launching Streamlit App..."
streamlit run dashboard_app.py
