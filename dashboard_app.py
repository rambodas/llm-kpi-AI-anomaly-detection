import streamlit as st
import pandas as pd
from gpt4all import GPT4All
from io import StringIO

# --------- Config ---------
st.set_page_config(layout="wide")
st.title("🌍 Multi-Region Login Spike Anomaly Detector (Local GGUF LLM)")

# --------- Constants ---------
MODEL_PATH = "C:/Users/dasra/OneDrive/Desktop/anomaly_detection/models/mistral-7b-openorca.Q4_K_M.gguf"
DATA_PATH = "dummy_login_data_multi_region.csv"

# --------- Load Data ---------
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH, parse_dates=["date"])

df = load_data()

# --------- Anomaly Detection Logic ---------
grouped = df.groupby(["date", "region"]).size().reset_index(name="logins")
grouped["prev_day_logins"] = grouped.groupby("region")["logins"].shift(1)
grouped["spike_ratio"] = grouped["logins"] / grouped["prev_day_logins"]

# Catch spikes across all non-India regions
anomalies = grouped[
    (grouped["region"] != "India") &
    (grouped["logins"] >= 50) &
    (grouped["spike_ratio"] >= 3)
].copy()

# --------- Load Local LLM Model ---------
@st.cache_resource
def load_llm_model():
    return GPT4All(model_name=MODEL_PATH, model_type="llama", allow_download=False)

# --------- RCA Table Display ---------
def display_wrapped_scrollable_table(df):
    html = df.to_html(classes='table table-striped', escape=False, index=False)
    wrapped_html = f"""
    <div style='overflow-x: auto; max-width: 100%;'>
        <style>
            th, td {{
                text-align: left;
                vertical-align: top;
                white-space: normal !important;
                word-wrap: break-word !important;
                max-width: 400px;
                padding: 8px;
                font-size: 14px;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                table-layout: fixed;
            }}
        </style>
        {html}
    </div>
    """
    st.markdown(wrapped_html, unsafe_allow_html=True)

# --------- Generate RCA with Local GGUF Model ---------
if not anomalies.empty:
    st.subheader("📌 Detected Anomalies with RCA Suggestions")

    model = load_llm_model()
    rca_list = []

    with model.chat_session():
        for idx, row in anomalies.iterrows():
            prompt = (
                f"There was a sudden spike in login activity from {row['region']} on {row['date'].date()}. "
                f"Logins increased from {int(row['prev_day_logins'])} to {int(row['logins'])}, "
                f"which is a {row['spike_ratio']:.2f}x jump. "
                f"What are some possible business reasons for this spike?"
            )
            st.write(f"🧠 Thinking about {row['region']} on {row['date'].date()}...")
            response = model.generate(prompt, max_tokens=100)
            rca_list.append(response.strip())

    anomalies["RCA_Suggestion"] = rca_list

    # --------- Download Button ---------
    csv_buffer = StringIO()
    anomalies.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()

    st.download_button(
        label="⬇️ Download Anomaly Report as CSV",
        data=csv_data,
        file_name="multi_region_anomaly_report.csv",
        mime="text/csv"
    )

    # --------- Display Anomaly Table ---------
    with st.expander("🔍 View Detailed Anomalies"):
        display_wrapped_scrollable_table(anomalies[[
            "date", "region", "logins", "prev_day_logins", "spike_ratio", "RCA_Suggestion"
        ]])
else:
    st.info("✅ No anomalies detected in non-India regions (3x spike + ≥50 logins)")

# --------- Login Trends Chart ---------
st.subheader("📊 Login Trends by Region")
for region in df["region"].unique():
    st.write(f"**{region}**")
    region_data = grouped[grouped["region"] == region]
    st.line_chart(region_data.set_index("date")["logins"], height=250)
