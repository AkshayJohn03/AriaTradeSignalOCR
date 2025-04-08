# screen_capture.py
import mss
import numpy as np
from PIL import Image
from config import CAPTURE_REGION

def capture_screen():
    with mss.mss() as sct:
        monitor = {
            "left": CAPTURE_REGION[0],
            "top": CAPTURE_REGION[1],
            "width": CAPTURE_REGION[2],
            "height": CAPTURE_REGION[3],
        }
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
        return img
