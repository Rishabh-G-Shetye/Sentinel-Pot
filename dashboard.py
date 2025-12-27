import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="Sentinel-Pot Dashboard", layout="wide", page_icon="🛡️")

st.title("🛡️ Sentinel-Pot: Live Threat Intelligence")
st.markdown("### Automated Deception & Attack Mapping")


def load_data():
    try:
        with open("enriched_attacks.json", "r") as f:
            return pd.DataFrame(json.load(f))
    except Exception:
        return pd.DataFrame()


# This "fragment" decorator tells Streamlit to only rerun this function every 2 seconds
@st.fragment(run_every="2s")
def render_dashboard():
    df = load_data()

    if not df.empty:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Global Attack Origins")
            # The map is now outside the metrics for better layout
            st.map(df[['lat', 'lon']])

        with col2:
            st.subheader("Quick Stats")
            st.metric("Total Attacks", len(df))
            st.metric("Unique IPs", df['ip'].nunique())

            st.subheader("Top Passwords")
            # Fixed the deprecation here: use_container_width -> width='stretch'
            st.bar_chart(df['password'].value_counts().head(5), width='stretch')

        st.subheader("Recent Activity")
        # Fixed the deprecation here: use_container_width -> width='stretch'
        st.dataframe(
            df[['timestamp', 'ip', 'country', 'username', 'password', 'isp']].tail(10),
            width='stretch'
        )
    else:
        st.info("Sentinel-Pot is active. Waiting for incoming data...")


# Call the fragmented function
render_dashboard()