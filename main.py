# main.py

import time
import os
import shutil
import json
from datetime import datetime

from utils.screen_capture import capture_screen_and_ocr, clean_temp_images
from ocr_reader import extract_text
from analyzer import parse_option_data
from notifier import send_telegram_message
from option_chain_fetcher import fetch_options
from signal_logger import log_signal
from ai_verifier import verify_with_ai, is_ollama_available

RUNTIME_CONFIG_PATH = "runtime_config.json"
IMG_PATH = "web_dashboard/static/latest.png"
TEMP_DIR = './temp/ocr_images/'

def load_config():
    if os.path.exists(RUNTIME_CONFIG_PATH):
        with open(RUNTIME_CONFIG_PATH) as f:
            return json.load(f)
    return {"daily_invest": 2000, "use_ai": True}

def fallback_filter(options, ocr_text):
    filtered = []
    for opt in options:
        if (
            opt.get("premium") and 5 <= opt["premium"] <= 40 and
            str(opt["strike"]) in ocr_text and
            opt.get("volume", 0) >= 3000
        ):
            filtered.append({
                "type": opt["type"],
                "strike": opt["strike"],
                "premium": opt["premium"],
                "volume": opt["volume"],
                "confidence": 0.65,
                "reason": "Fallback filter"
            })
    return filtered

def broadcast_to_ui(signals, image_path, ocr_text):
    print("[📻] UI updated with latest scan.")

def run():
    print("[🚀] Live Trade Assistant Running...\n")
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    while True:
        config = load_config()
        DAILY_INVEST = int(config.get("daily_invest", 2000))
        USE_AI = config.get("use_ai", True)
        PER_TRADE = DAILY_INVEST / 2

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        image_path, ocr_text = capture_screen_and_ocr()
        clean_temp_images()

        try:
            shutil.copy(image_path, TEMP_DIR)
        except Exception as e:
            print(f"[❌] Image copy failed: {e}")

        options = fetch_options()
        if not options:
            print(f"[{timestamp}] ❌ No data fetched from NSE.")
            time.sleep(1)
            continue

        print(f"[{timestamp}] ✅ Fetched {len(options)} options from NSE")

        if USE_AI and is_ollama_available():
            print("[🤖] Using AI signal verification...")
            signals = verify_with_ai(options, ocr_text)
        else:
            signals = fallback_filter(options, ocr_text)

        final_signals = []
        for sig in signals:
            summary = f"{sig['type']} ₹{sig['premium']} | Strike {sig['strike']} | Vol {sig['volume']}"
            output = (
                f"🟢 {summary}\n"
                f"📊 Confidence: {int(sig['confidence'] * 100)}%\n"
                f"💰 Return: ₹{PER_TRADE * 0.1:.0f}–₹{PER_TRADE * 0.25:.0f}\n"
                f"🧠 Reason: {sig.get('reason', 'N/A')}"
            )
            print(output)
            send_telegram_message(output)
            log_signal(output, sig['confidence'], sig.get("reason", "N/A"))
            final_signals.append(output)

        if not final_signals:
            print("[⏳] No valid trades found.")

        broadcast_to_ui(final_signals, image_path, ocr_text)
        time.sleep(0.5)

if __name__ == "__main__":
    run()
