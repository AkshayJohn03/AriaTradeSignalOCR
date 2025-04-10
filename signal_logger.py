# signal_logger.py

import json
import os
from datetime import datetime

LOG_PATH = 'logs/trade_log.json'

def log_signal(signal, confidence=0.8, comment=""):
    """Appends a trade signal to a persistent JSON log."""
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    log_entry = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "signal": signal,
        "confidence": confidence,
        "comment": comment
    }

    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'r') as f:
            try:
                logs = json.load(f)
            except:
                logs = []
    else:
        logs = []

    logs.append(log_entry)

    with open(LOG_PATH, 'w') as f:
        json.dump(logs, f, indent=2)
