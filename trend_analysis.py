# File: trend_analysis.py

import statistics

def apply_supertrend(premiums, period=7, multiplier=3):
    if len(premiums) < period:
        return None

    atr = statistics.mean([abs(p - premiums[i - 1]) for i, p in enumerate(premiums[1:], 1)])
    hl2 = premiums[-1]  # Use current price as midpoint for simplicity
    upper_band = hl2 + multiplier * atr
    lower_band = hl2 - multiplier * atr
    trend = 'Buy' if premiums[-1] > upper_band else 'Sell' if premiums[-1] < lower_band else 'Hold'
    return trend

def apply_ema_strategy(premiums, short_period=5, long_period=15):
    if len(premiums) < long_period:
        return None

    short_ema = statistics.mean(premiums[-short_period:])
    long_ema = statistics.mean(premiums[-long_period:])
    return 'Buy' if short_ema > long_ema else 'Sell'

def analyze_trend(option_history):
    results = []
    for opt in option_history:
        if len(opt['history']) < 15:
            continue
        supertrend = apply_supertrend(opt['history'])
        ema_trend = apply_ema_strategy(opt['history'])
        if supertrend == 'Buy' and ema_trend == 'Buy':
            results.append(f"Strong Buy Signal: {opt['strike']} ₹{opt['history'][-1]}")
        elif supertrend == 'Sell' and ema_trend == 'Sell':
            results.append(f"Strong Sell Signal: {opt['strike']} ₹{opt['history'][-1]}")
    return results
