# dev_tool.py

from screen_capture import capture_screen
from ocr_reader import extract_text
from analyzer import parse_option_data

img = capture_screen()
text = extract_text(img)
signals = parse_option_data(text)

print("\n[🧠 RAW OCR TEXT]\n", text)
print("\n[💡 FILTERED SIGNALS]\n", signals)
