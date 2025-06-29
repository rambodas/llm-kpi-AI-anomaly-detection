@echo off
echo 🔁 Creating virtual environment...
python -m venv env
call env\Scripts\activate

echo ⬇️ Installing dependencies...
pip install -r requirements.txt

echo 🚀 Launching Streamlit App...
streamlit run dashboard_app.py
pause
