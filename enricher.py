import json
import time
import random
from faker import Faker

fake = Faker()

# List of real global coordinates to make the map look busy/realistic
SIMULATED_LOCATIONS = [
    {"country": "United States", "city": "New York", "lat": 40.7128, "lon": -74.0060, "isp": "Verizon"},
    {"country": "China", "city": "Beijing", "lat": 39.9042, "lon": 116.4074, "isp": "China Telecom"},
    {"country": "Russia", "city": "Moscow", "lat": 55.7558, "lon": 37.6173, "isp": "Rostelecom"},
    {"country": "Germany", "city": "Berlin", "lat": 52.5200, "lon": 13.4050, "isp": "Deutsche Telekom"},
    {"country": "Brazil", "city": "São Paulo", "lat": -23.5505, "lon": -46.6333, "isp": "Vivo"},
]


def generate_fake_attack():
    loc = random.choice(SIMULATED_LOCATIONS)

    # Add "Jitter" (random noise) so markers don't overlap perfectly
    jitter_lat = random.uniform(-0.5, 0.5)
    jitter_lon = random.uniform(-0.5, 0.5)

    return {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ip": fake.ipv4_public(),
        "username": random.choice(["admin", "root", "support", "user", "guest"]),
        "password": fake.password(length=8),
        "event": "simulated_attack",
        "country": loc["country"],
        "city": loc["city"],
        "lat": loc["lat"] + jitter_lat,  # Apply jitter
        "lon": loc["lon"] + jitter_lon,  # Apply jitter
        "isp": loc["isp"]
    }


def run_enrichment(simulation_mode=True):
    print(f"[*] Sentinel-Pot Enricher started (Simulation: {simulation_mode})")

    while True:
        try:
            # 1. Read existing data
            try:
                with open("enriched_attacks.json", "r") as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = []

            # 2. Add fake data if simulation is ON
            if simulation_mode:
                new_attack = generate_fake_attack()
                data.append(new_attack)
                print(f"[+] Simulated attack from {new_attack['ip']} ({new_attack['country']})")

            # 3. Save back to file
            with open("enriched_attacks.json", "w") as f:
                json.dump(data, f, indent=4)

            time.sleep(3)  # Add a new fake attack every 3 seconds
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)


if __name__ == "__main__":
    run_enrichment(simulation_mode=True)