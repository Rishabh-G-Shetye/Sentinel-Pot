import paramiko
import time
import random
import sys

# Configuration
TARGET_IP = "127.0.0.1"
TARGET_PORT = 2222

# Data Sources
USERNAMES = ["admin", "root", "user", "support", "oracle", "test", "guest", "info"]
PASSWORDS = ["123456", "password", "admin", "root", "toor", "qwerty", "letmein", "111111"]


def attempt_login(username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # We expect this to fail (Authentication failed) or error out
        client.connect(TARGET_IP, port=TARGET_PORT, username=username, password=password, timeout=3)
    except paramiko.AuthenticationException:
        print(f"[-] Failed login sent: {username}:{password}")
    except Exception as e:
        print(f"[!] Connection Error (Pot might be down): {e}")
    finally:
        client.close()


def rapid_fire(count=50):
    print(f"[*] Launching {count} random attacks...")
    for i in range(count):
        u = random.choice(USERNAMES)
        p = f"{random.choice(PASSWORDS)}{random.randint(1, 999)}"
        attempt_login(u, p)
        time.sleep(0.1)  # Very fast


def dictionary_attack():
    target_user = "admin"
    print(f"[*] Starting dictionary attack against user '{target_user}'...")
    for pw in PASSWORDS:
        attempt_login(target_user, pw)
        time.sleep(0.5)


def stealth_mode():
    print("[*] Starting slow/stealth mode (CTRL+C to stop)...")
    try:
        while True:
            u = random.choice(USERNAMES)
            p = random.choice(PASSWORDS)
            attempt_login(u, p)
            wait = random.randint(2, 10)
            print(f"[*] Waiting {wait}s...")
            time.sleep(wait)
    except KeyboardInterrupt:
        print("\n[*] Stopping.")


if __name__ == "__main__":
    print("--- Sentinel Attack Simulator ---")
    print("1. Rapid Fire (50 random bursts)")
    print("2. Dictionary Attack (Common passwords)")
    print("3. Stealth Mode (Continuous slow attacks)")

    choice = input("Select attack mode (1-3): ")

    if choice == '1':
        rapid_fire()
    elif choice == '2':
        dictionary_attack()
    elif choice == '3':
        stealth_mode()
    else:
        print("Invalid selection")