# web_dashboard/replay_viewer.py

import os
from flask import Flask, send_from_directory, jsonify
from datetime import datetime

REPLAY_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'temp', 'ocr_images')

def get_recent_images(limit=30):
    files = [f for f in os.listdir(REPLAY_FOLDER) if f.endswith('.png')]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(REPLAY_FOLDER, x)), reverse=True)
    return files[:limit]

def register_replay_routes(app):
    @app.route('/replay-images')
    def replay_images():
        image_files = get_recent_images()
        return jsonify([f"/replay/{name}" for name in image_files])

    @app.route('/replay/<filename>')
    def serve_replay_image(filename):
        return send_from_directory(REPLAY_FOLDER, filename)
