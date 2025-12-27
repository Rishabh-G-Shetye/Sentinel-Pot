# 🛡️ Sentinel-Pot
**Sentinel-Pot** is a deceptive threat intelligence honeypot designed to capture, enrich, and visualize real-time cyber attacks.

## 🚀 Features
- **SSH Deception:** Mimics a vulnerable server to capture brute-force attempts.
- **Automated Enrichment:** Uses IP Geolocation APIs to map attacker origins.
- **Live Dashboard:** Real-time visualization using Streamlit and world maps.
- **Simulation Mode:** Generates global attack data for demonstration purposes.

## 🛠️ Tech Stack
- Python (Paramiko, Requests)
- Streamlit (UI/UX)
- Pandas (Data Processing)

## 🔧 Installation
1. Clone the repo: `git clone https://github.com/yourusername/Sentinel-Pot.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the components in separate terminals:
   - `python honeypot.py`
   - `python enricher.py`
   - `streamlit run dashboard.py`