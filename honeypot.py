import socket
import threading
import paramiko
import json
from datetime import datetime

# Load a host key (PyCharm terminal: ssh-keygen -t rsa -f server.key)
HOST_KEY = paramiko.RSAKey.generate(2048)


class SSHServer(paramiko.ServerInterface):
    def __init__(self, client_ip):
        self.client_ip = client_ip

    def check_auth_password(self, username, password):
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ip": self.client_ip,
            "username": username,
            "password": password,
            "event": "login_attempt"
        }
        print(f"[!] Attack from {self.client_ip}: {username}:{password}")

        with open("attacks.json", "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        return paramiko.AUTH_FAILED  # Always fail to keep them out


def handle_client(client_sock):
    client_ip = client_sock.getpeername()[0]
    transport = paramiko.Transport(client_sock)
    transport.add_server_key(HOST_KEY)
    server = SSHServer(client_ip)
    try:
        transport.start_server(server=server)
    except Exception as e:
        print(f"Error: {e}")


def start_pot(port=2222):  # Use 2222 to avoid needing sudo/root
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', port))
    sock.listen(100)
    print(f"[*] Sentinel-Pot SSH active on port {port}...")

    while True:
        client_sock, addr = sock.accept()
        threading.Thread(target=handle_client, args=(client_sock,)).start()


if __name__ == "__main__":
    start_pot()