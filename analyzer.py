# analyzer.py

import re
from config import PREMIUM_MIN, PREMIUM_MAX, MIN_VOLUME

def parse_option_data(ocr_text):
    """
    Extracts option data lines from OCR string and filters based on premium and volume.
    Looks for patterns like: 'NIFTY 19500 CE ₹28 105000'
    """
    lines = ocr_text.splitlines()
    trade_signals = []

    for line in lines:
        # Look for a line that might include a premium and a volume
        matches = re.findall(r'([A-Z]+[\s\d]{4,}[\sPE|CE]*)\s.*?₹?(\d+\.\d+|\d+)[^\d]*(\d{3,})', line)
        for match in matches:
            name, premium, volume = match
            try:
                premium = float(premium)
                volume = int(volume.replace(",", ""))

                if PREMIUM_MIN <= premium <= PREMIUM_MAX and volume >= MIN_VOLUME:
                    signal = f"{name.strip()} | ₹{premium} | Volume: {volume}"
                    trade_signals.append(signal)
            except ValueError:
                continue

    return trade_signals
