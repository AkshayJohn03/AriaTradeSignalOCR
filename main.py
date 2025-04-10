# main.py

import time
import os
import shutil
from datetime import datetime

# Imports from your structured project
from utils.screen_capture import capture_screen_and_ocr, clean_temp_images
from ocr_reader import extract_text
from analyzer import parse_option_data
from notifier import send_telegram_message
from option_chain_fetcher import fetch_options
from signal_logger import log_signal
from ai_verifier import verify_with_ai, is_ollama_available
# from flask_socketio import SocketIO  # For future UI push integration

IMG_PATH = "web_dashboard/static/latest.png"
TEMP_DIR = './temp/ocr_images/'
LOG_PATH = 'logs/trade_log.json'

# Adjustable user values
DAILY_INVEST = 2000
PER_TRADE = DAILY_INVEST / 2
USE_AI = True  # Toggled automatically if Ollama not available

# Helper: Basic fallback signal filter
def basic_signal_filter(options, ocr_text):
    filtered = []
    for opt in options:
        if (
            opt.get("premium") and 10 <= opt["premium"] <= 30 and
            str(opt["strike"]) in ocr_text and
            opt.get("volume", 0) > 10000
        ):
            filtered.append(f"{opt['type']} ₹{opt['premium']} Strike: {opt['strike']} Vol: {opt['volume']}")
    return filtered

# Optional UI broadcast
def broadcast_to_ui(signals, image_path, ocr_text):
    print("[📻] Broadcasting to UI (not yet implemented)")

def run():
    print("[🚀] Live Trade Assistant Running...\n")

    # Ensure temp/log dirs exist
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    while True:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 1. Capture & OCR
        image_path, ocr_text = capture_screen_and_ocr()
        clean_temp_images()
        try:
            shutil.copy(image_path, TEMP_DIR)
        except Exception as e:
            print(f"[❌] Image copy failed: {e}")

        # 2. Option Chain Fetch
        options = fetch_options()
        if not options:
            print(f"[{timestamp}] ❌ No data fetched from NSE.")
            time.sleep(1)
            continue
        else:
            print(f"[{timestamp}] ✅ Fetched {len(options)} options.")

        # 3. Signal Verification
        if USE_AI and is_ollama_available():
            signals = verify_with_ai(options, ocr_text)
        else:
            signals = basic_signal_filter(options, ocr_text)

        # 4. Logging & Telegram
        final_signals = []
        for sig in signals:
            signal_text = f"🟢 {sig}\n💰 Range: ₹{PER_TRADE * 0.1:.0f}–₹{PER_TRADE * 0.25:.0f}\n⏱️ {timestamp}"
            print(signal_text)
            send_telegram_message(signal_text)
            log_signal(sig, 0.75, "AI Verified" if USE_AI else "Fallback Filter")
            final_signals.append(signal_text)

        if not final_signals:
            print("[⏳] No valid trades found this cycle.")

        broadcast_to_ui(final_signals, image_path, ocr_text)

        time.sleep(1)

if __name__ == "__main__":
    run()
