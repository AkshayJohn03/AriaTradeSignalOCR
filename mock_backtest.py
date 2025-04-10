# mock_backtest.py

import os
from PIL import Image
from ocr_reader import extract_text
from option_chain_fetcher import fetch_options
from ai_verifier import verify_with_ai, is_ollama_available
from signal_logger import log_signal

MOCK_FOLDER = "./mock_data/screenshots"

def run_backtest():
    files = [f for f in os.listdir(MOCK_FOLDER) if f.endswith('.png')]
    if not files:
        print("❌ No screenshots found in mock_data/screenshots/")
        return

    options = fetch_options()
    if not options:
        print("❌ Option chain could not be fetched. Backtest aborted.")
        return

    for fname in sorted(files):
        path = os.path.join(MOCK_FOLDER, fname)
        print(f"\n[📂] Processing: {fname}")

        img = Image.open(path)
        text = extract_text(img)

        if is_ollama_available():
            signals = verify_with_ai(options, text)
        else:
            signals = []
            for opt in options:
                if str(opt["strike"]) in text and 10 <= opt["premium"] <= 30:
                    signals.append(f"{opt['type']} Strike {opt['strike']} ₹{opt['premium']}")

        if signals:
            for sig in signals:
                print(f"🟢 Signal: {sig}")
                log_signal(f"[MockTest:{fname}] {sig}", 0.85, "Backtest")
        else:
            print("⏳ No valid signals from this screenshot.")

if __name__ == "__main__":
    run_backtest()
