# config.py
import os

# Screen capture region (left, top, width, height)
CAPTURE_REGION = (1, 90, 758, 1192)

# OCR configuration
if os.name == 'nt':  # Windows
    TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:  # macOS or Linux
    TESSERACT_PATH = r"/opt/homebrew/Cellar/tesseract/5.5.0_1/bin/tesseract"

# Telegram bot
TELEGRAM_BOT_TOKEN = "7208650446:AAEEVc5xMgFVm7nOsAQxH-SgJqxFY_UWUMI"
TELEGRAM_CHAT_ID = "731344061" #https://t.me/userinfobot

# Trade filters
PREMIUM_MIN = 10
PREMIUM_MAX = 30
MIN_VOLUME = 10000
