import json
import time
import random
import os
from datetime import datetime

# MITRE ATT&CK Mapping
MITRE_MAP = {
    "login_attempt": "T1110 (Brute Force)",
    "web_login_attempt": "T1078 (Valid Accounts)",
    "simulated_attack": "T1595 (Active Scanning)"
}


def run_enrichment():
    print("[*] Enricher Service Started...")

    # Ensure files exist
    if not os.path.exists("/app/attacks.json"):
        with open("/app/attacks.json", "w") as f: f.write("")

    # Track position in raw file to avoid duplicates
    last_pos = 0

    while True:
        new_entries = []

        try:
            # Read only NEW lines from attacks.json
            with open("/app/attacks.json", "r") as f:
                f.seek(last_pos)
                lines = f.readlines()
                last_pos = f.tell()

            if lines:
                print(f"[*] Processing {len(lines)} new events...")

                # Load existing enriched data to append to
                existing_data = []
                if os.path.exists("/app/enriched_attacks.json"):
                    try:
                        with open("/app/enriched_attacks.json", "r") as f:
                            existing_data = json.load(f)
                    except:
                        existing_data = []

                for line in lines:
                    try:
                        entry = json.loads(line.strip())
                        # Add Intelligence
                        entry["mitre"] = MITRE_MAP.get(entry.get("event"), "T1059")
                        entry["risk_score"] = random.randint(60, 100)
                        entry["country"] = "Unknown"  # Placeholder for GeoIP
                        entry["lat"] = random.uniform(-50, 50)  # Random for demo viz
                        entry["lon"] = random.uniform(-100, 100)
                        existing_data.append(entry)
                    except json.JSONDecodeError:
                        continue

                # Write updated enriched data
                with open("/app/enriched_attacks.json", "w") as f:
                    json.dump(existing_data, f, indent=4)

            time.sleep(2)

        except Exception as e:
            print(f"[!] Enricher Error: {e}")
            time.sleep(2)


if __name__ == "__main__":
    run_enrichment()