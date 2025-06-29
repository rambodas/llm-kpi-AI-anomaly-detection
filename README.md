# 🔍 LLM KPI Anomaly Detector

A Streamlit-based anomaly detection dashboard that detects sudden spikes in KPI metrics like login activity across regions. It uses a **local GGUF LLM (e.g., Mistral via gpt4all)** to generate root cause analysis (RCA) suggestions in natural language.

---

## 📌 Features

- Detects login spikes by region (e.g., Dubai, Mauritius, Sri Lanka)
- Uses 3x day-over-day increase + 50 login minimum threshold
- Generates RCA suggestions using a local quantized model
- Visualizes login trends across regions
- Supports exporting anomaly reports as CSV

---

## 🚀 How to Run

1. Clone this repo  
2. Download a GGUF model (e.g., Mistral or TinyLlama)  
3. Place it in the `models/` folder  
4. Then run:

```bash
# On Linux/Mac
bash run_app.sh

# On Windows
run_app.bat
```

---

## 🧠 Example Prompt to LLM

> "There was a sudden spike in login activity from Dubai on 2025-06-10.  
> Logins increased from 20 to 170, which is a 8.5x jump.  
> What are some possible business reasons for this spike?"

---

## 📂 Folder Structure

```
.
├── dashboard_app.py
├── dummy_data.py
├── dummy_login_data_multi_region.csv
├── models/
│   └── mistral-7b-openorca.Q4_K_M.gguf
├── requirements.txt
├── run_app.sh
├── run_app.bat
├── .gitignore
└── README.md
```

---

## 📜 License

MIT
