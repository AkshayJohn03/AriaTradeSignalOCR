# analyzer.py
from config import PREMIUM_MIN, PREMIUM_MAX, MIN_VOLUME

def parse_option_data(raw_text):
    lines = raw_text.splitlines()
    buy_signals = []
    for line in lines:
        if "CE" in line or "PE" in line:
            parts = line.split()
            try:
                premium = float(parts[-2])
                volume = int(parts[-1].replace(",", ""))
                if PREMIUM_MIN <= premium <= PREMIUM_MAX and volume >= MIN_VOLUME:
                    buy_signals.append(line)
            except:
                continue
    return buy_signals
