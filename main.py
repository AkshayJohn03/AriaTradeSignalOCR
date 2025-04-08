# main.py
import time
from screen_capture import capture_screen
from ocr_reader import extract_text
from analyzer import parse_option_data
from notifier import send_telegram_message

def run():
    print("[+] Starting Trade Signal Monitor...")
    while True:
        image = capture_screen()
        text = extract_text(image)
        signals = parse_option_data(text)
        if signals:
            message = "\n".join(["Trade Opportunity Found:"] + signals)
            send_telegram_message(message)
            print("[✔] Trade signal sent!")
        time.sleep(30)  # Adjust frequency here

if __name__ == "__main__":
    run()
