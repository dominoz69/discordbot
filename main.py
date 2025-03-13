from flask import Flask, render_template, jsonify
import os
import subprocess
import threading

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
def status():
    return jsonify({
        "status": "running",
        "prefix": "@"
    })

def run_bot():
    subprocess.Popen(["python", "bot.py"])

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    app.run(host='0.0.0.0', port=5000, debug=True)