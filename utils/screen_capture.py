# utils/screen_capture.py

import mss
import uuid
import os
import pytesseract
from PIL import Image
from screeninfo import get_monitors
from config import CAPTURE_REGION, TESSERACT_PATH

STATIC_IMAGE_PATH = "web_dashboard/static/latest.png"
TEMP_DIR = "./temp/ocr_images/"
MAX_TEMP_IMAGES = 3600  # keep only last 1 hour at 1 image/second

# Ensure temp folder exists
os.makedirs(TEMP_DIR, exist_ok=True)
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def capture_screen():
    """Capture from a fixed region on screen 2 (portrait) if available."""
    monitors = get_monitors()
    target_screen = monitors[1] if len(monitors) > 1 else monitors[0]  # Use screen 2 if available
    left_offset = target_screen.x + CAPTURE_REGION[0]
    top_offset = target_screen.y + CAPTURE_REGION[1]

    monitor = {
        "top": top_offset,
        "left": left_offset,
        "width": CAPTURE_REGION[2],
        "height": CAPTURE_REGION[3]
    }

    with mss.mss() as sct:
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
        return img

def capture_screen_and_ocr():
    """
    Captures the screen:
    - Saves the latest image to web_dashboard/static/latest.png (UI)
    - Stores image to /temp/ocr_images/ for hourly buffer
    - Returns OCR text and image path
    """
    image = capture_screen()

    # Save latest for UI
    image.save(STATIC_IMAGE_PATH)

    # Save temp for buffer
    filename = os.path.join(TEMP_DIR, f"{uuid.uuid4().hex}.png")
    image.save(filename)

    # Cleanup old images if needed
    clean_temp_images(limit=MAX_TEMP_IMAGES)

    text = pytesseract.image_to_string(image)
    return STATIC_IMAGE_PATH, text

def clean_temp_images(limit=3600):
    """Keeps only the most recent N images in TEMP_DIR, deletes the oldest first."""
    files = [os.path.join(TEMP_DIR, f) for f in os.listdir(TEMP_DIR) if f.endswith(".png")]
    if len(files) <= limit:
        return

    files.sort(key=os.path.getmtime)  # sort oldest to newest
    for file in files[:-limit]:
        try:
            os.remove(file)
        except Exception as e:
            print(f"[⚠️] Failed to delete {file}: {e}")