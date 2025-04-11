# option_chain_fetcher.py

import requests
import datetime
import time

def fetch_options(symbol="NIFTY"):
    print("[🌐] Fetching NSE Option Chain...")

    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://www.nseindia.com/option-chain",
        "X-Requested-With": "XMLHttpRequest"
    }

    base_url = "https://www.nseindia.com"
    try:
        session.get(base_url, headers=headers, timeout=5)
    except Exception as e:
        print("[❌] Failed to reach NSE:", e)
        return []

    url = f"{base_url}/api/option-chain-indices?symbol={symbol}"
    try:
        response = session.get(url, headers=headers, timeout=5)
        data = response.json()
    except Exception as e:
        print("[❌] Failed to parse option chain data:", e)
        return []

    today = datetime.date.today()
    nearest_thursday = today + datetime.timedelta((3 - today.weekday()) % 7)
    nearest_expiry = nearest_thursday.strftime("%d-%b-%Y").upper()

    chain = []
    count = 0
    for item in data.get("records", {}).get("data", []):
        if item.get("expiryDate") != nearest_expiry:
            continue
        for option_type in ["CE", "PE"]:
            record = item.get(option_type)
            if record:
                chain.append({
                    "type": option_type,
                    "strike": record.get("strikePrice"),
                    "premium": record.get("lastPrice"),
                    "volume": record.get("totalTradedVolume"),
                    "oi": record.get("openInterest")
                })
                count += 1

    if count > 0:
        print(f"[📈] Received {count} options from NSE for {nearest_expiry}")
    else:
        print("[⚠️] No options found for the nearest expiry.")

    return chain

def get_latest_filtered_options():
    """Return simplified CE/PE options between ₹5-40 premium."""
    raw = fetch_options()
    return [
        o for o in raw
        if o.get("premium") and 5 <= o["premium"] <= 40 and o.get("volume", 0) > 3000
    ]