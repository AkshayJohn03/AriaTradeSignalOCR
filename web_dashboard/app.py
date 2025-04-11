from flask import Flask, render_template, send_from_directory, jsonify, request
import os
import time
import json

app = Flask(__name__)

SIGNAL_LOG = os.path.join(os.path.dirname(__file__), '..', 'logs', 'trade_log.json')
OCR_IMAGE = os.path.join(os.path.dirname(__file__), 'static', 'latest.png')
OCR_REPLAY_DIR = os.path.join(os.path.dirname(__file__), '..', 'temp', 'ocr_images')
RUNTIME_CONFIG = os.path.join(os.path.dirname(__file__), '..', 'runtime_config.json')

@app.route('/')
def dashboard():
    try:
        with open(SIGNAL_LOG, 'r') as f:
            logs = json.load(f)
    except:
        logs = []

    latest_signals = logs[-10:][::-1]
    try:
        with open(RUNTIME_CONFIG) as f:
            config = json.load(f)
            budget = int(config.get("daily_invest", 2000))
            use_ai = config.get("use_ai", True)
    except:
        budget = 2000
        use_ai = True

    invested = len(latest_signals) * 1000
    remaining = budget - invested

    return render_template(
        "index.html",
        signals=latest_signals,
        invested=invested,
        remaining=remaining,
        budget=budget,
        use_ai=use_ai,
        image_timestamp=int(time.time())
    )

@app.route('/image')
def image():
    return send_from_directory('static', 'latest.png')

@app.route('/replay-images')
def replay_images():
    if not os.path.exists(OCR_REPLAY_DIR):
        return jsonify([])

    files = sorted([
        f for f in os.listdir(OCR_REPLAY_DIR) if f.endswith(".png")
    ], key=lambda x: os.path.getmtime(os.path.join(OCR_REPLAY_DIR, x)), reverse=True)

    urls = [f"/replay/{f}" for f in files[:30]]
    return jsonify(urls)

@app.route('/replay/<filename>')
def serve_image(filename):
    return send_from_directory(OCR_REPLAY_DIR, filename)

@app.route('/mock-options')
def mock_options():
    try:
        with open(os.path.join(os.path.dirname(__file__), '..', 'temp', 'latest_options.json')) as f:
            return jsonify(json.load(f))
    except:
        return jsonify([])

@app.route('/set-config', methods=["POST"])
def set_config():
    try:
        data = request.json
        with open(RUNTIME_CONFIG, "w") as f:
            json.dump(data, f, indent=2)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
