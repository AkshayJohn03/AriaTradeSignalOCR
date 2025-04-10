# web_dashboard/app.py

from flask import Flask, render_template, send_from_directory
import os
import time
import json

app = Flask(__name__)

SIGNAL_LOG = os.path.join(os.path.dirname(__file__), '..', 'logs', 'trade_log.json')
OCR_IMAGE = os.path.join(os.path.dirname(__file__), 'static', 'latest.png')

@app.route('/')
def dashboard():
    try:
        with open(SIGNAL_LOG, 'r') as f:
            logs = json.load(f)
    except:
        logs = []

    latest_signals = logs[-10:][::-1]  # Show last 10 logs
    total_invest = 2000
    invested = len(latest_signals) * 1000  # mock value
    remaining = total_invest - invested

    # Mock values for profit and win rate (replace with actual calculations if available)
    profit = 500  # Example profit value
    win_rate = 75  # Example win rate percentage

    return render_template(
        "index.html",
        signals=latest_signals,
        invested=invested,
        remaining=remaining,
        profit=profit,
        win_rate=win_rate,
        image_timestamp=int(time.time())  # Force image refresh
    )

@app.route('/image')
def image():
    return send_from_directory('static', 'latest.png')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)