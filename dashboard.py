import streamlit as st
import pandas as pd
import json
import time
import os

st.set_page_config(page_title="Sentinel-Pot SOC", layout="wide", page_icon="🛡️")

# File path inside Docker
DATA_FILE = "/app/enriched_attacks.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame()
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return pd.DataFrame(data)
    except:
        return pd.DataFrame()


# --- HEADER ---
st.title("🛡️ Sentinel-Pot: Threat Intelligence")
st.markdown("---")


# --- REAL-TIME CONTENT ---
@st.fragment(run_every="2s")
def dashboard_content():
    df = load_data()

    if df.empty:
        st.warning("⚠️ Waiting for live attack traffic... Connect via Ngrok.")
        return

    # KPIS
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Attacks Captured", len(df))
    c2.metric("Critical Threats", len(df[df['risk_score'] > 80]))
    c3.metric("Last Active", df.iloc[-1]['timestamp'] if not df.empty else "N/A")

    # MAP & CHARTS
    c_map, c_list = st.columns([2, 1])

    with c_map:
        st.subheader("Global Attack Origins")
        st.map(df[['lat', 'lon']], zoom=1)

    with c_list:
        st.subheader("Attack Vectors")
        st.bar_chart(df['event'].value_counts())

    # DATAFRAME
    st.subheader("Live Packet Logs")
    st.dataframe(
        df[['timestamp', 'ip', 'username', 'password', 'mitre']].tail(10),
        use_container_width=True
    )


dashboard_content()