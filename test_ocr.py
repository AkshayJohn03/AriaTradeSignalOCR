from screen_capture import capture_screen
from ocr_reader import extract_text

image = capture_screen()
text = extract_text(image)

print("\n--- Extracted Text ---\n")
print(text)
