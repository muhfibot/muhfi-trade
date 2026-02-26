"""
technical.py - TA Indicators Engine
RSI, MACD, MA (50/200), Bollinger Bands, Fibonacci
"""
import pandas as pd
import numpy as np
from config import RSI_PERIOD, MA_SHORT, MA_LONG, BB_PERIOD, BB_STD


def calc_rsi(series: pd.Series, period: int = RSI_PERIOD) -> float:
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = -delta.clip(upper=0).rolling(period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi.iloc[-1], 2)


def calc_macd(series: pd.Series):
    ema12 = series.ewm(span=12, adjust=False).mean()
    ema26 = series.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    histogram = macd - signal
    return round(macd.iloc[-1], 4), round(signal.iloc[-1], 4), round(histogram.iloc[-1], 4)


def calc_ma(series: pd.Series):
    ma50 = round(series.rolling(MA_SHORT).mean().iloc[-1], 4)
    ma200 = round(series.rolling(MA_LONG).mean().iloc[-1], 4) if len(series) >= MA_LONG else None
    return ma50, ma200


def calc_bollinger(series: pd.Series):
    ma = series.rolling(BB_PERIOD).mean()
    std = series.rolling(BB_PERIOD).std()
    upper = round((ma + BB_STD * std).iloc[-1], 4)
    mid = round(ma.iloc[-1], 4)
    lower = round((ma - BB_STD * std).iloc[-1], 4)
    return upper, mid, lower


def calc_fibonacci(high: float, low: float):
    diff = high - low
    levels = {
        "0.0": round(high, 4),
        "0.236": round(high - 0.236 * diff, 4),
        "0.382": round(high - 0.382 * diff, 4),
        "0.5": round(high - 0.5 * diff, 4),
        "0.618": round(high - 0.618 * diff, 4),
        "1.0": round(low, 4),
    }
    return levels


def analyze_technical(df: pd.DataFrame) -> dict:
    """
    Input: DataFrame dengan kolom ['open','high','low','close','volume']
    Output: dict dengan semua indikator + score teknikal (0-1)
    """
    close = df["close"]
    price = close.iloc[-1]

    rsi = calc_rsi(close)
    macd, signal, histogram = calc_macd(close)
    ma50, ma200 = calc_ma(close)
    bb_upper, bb_mid, bb_lower = calc_bollinger(close)
    fib = calc_fibonacci(df["high"].max(), df["low"].min())

    # Scoring logic
    score = 0.5  # neutral baseline
    signals = []

    # RSI
    if rsi < 30:
        score += 0.15
        signals.append(f"RSI oversold ({rsi})")
    elif rsi > 70:
        score -= 0.15
        signals.append(f"RSI overbought ({rsi})")

    # MACD
    if histogram > 0 and macd > signal:
        score += 0.10
        signals.append("MACD bullish crossover")
    elif histogram < 0 and macd < signal:
        score -= 0.10
        signals.append("MACD bearish crossover")

    # MA
    if ma50 and ma200:
        if price > ma50 > ma200:
            score += 0.10
            signals.append("Price > MA50 > MA200 (uptrend)")
        elif price < ma50 < ma200:
            score -= 0.10
            signals.append("Price < MA50 < MA200 (downtrend)")

    # Bollinger
    if price <= bb_lower:
        score += 0.10
        signals.append("Price at lower Bollinger Band (oversold)")
    elif price >= bb_upper:
        score -= 0.10
        signals.append("Price at upper Bollinger Band (overbought)")

    score = max(0.0, min(1.0, score))
    direction = "long" if score > 0.5 else "short"

    return {
        "price": price,
        "rsi": rsi,
        "macd": macd,
        "macd_signal": signal,
        "macd_histogram": histogram,
        "ma50": ma50,
        "ma200": ma200,
        "bb_upper": bb_upper,
        "bb_mid": bb_mid,
        "bb_lower": bb_lower,
        "fibonacci": fib,
        "score": round(score, 3),
        "direction": direction,
        "signals": signals,
    }
