# ocr_reader.py
import pytesseract
import cv2
import numpy as np
from config import TESSERACT_PATH
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def extract_text(image: Image.Image) -> str:
    open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(thresh)
    return text
