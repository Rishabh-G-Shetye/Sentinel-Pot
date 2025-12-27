from flask import Flask, request, render_template_string
import json
import os
from datetime import datetime

app = Flask(__name__)

LOGIN_PAGE = """
<html>
<head><title>Secure Gateway</title></head>
<body style="font-family: Arial; text-align: center; margin-top: 100px;">
    <h2>🛡️ Corporate Login</h2>
    <form method="POST">
        Username: <input type="text" name="username"><br><br>
        Password: <input type="password" name="password"><br><br>
        <input type="submit" value="Sign In">
    </form>
</body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ip": request.remote_addr,
            "username": request.form.get('username'),
            "password": request.form.get('password'),
            "event": "web_login_attempt"
        }

        with open("/app/attacks.json", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
            f.flush()

        return "<h1>500 Internal Server Error</h1>", 500
    return render_template_string(LOGIN_PAGE)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)