"""
data/fetcher.py - Market data fetcher (Binance + OANDA)
"""
import pandas as pd
import requests
from datetime import datetime
import config


def fetch_binance_klines(symbol: str = "BTCUSDT", interval: str = "1h", limit: int = 500) -> pd.DataFrame:
    """Fetch OHLCV dari Binance Futures (testnet jika paper mode)."""
    if config.BINANCE_TESTNET:
        base_url = "https://testnet.binancefuture.com"
    else:
        base_url = "https://fapi.binance.com"

    url = f"{base_url}/fapi/v1/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        raw = resp.json()
        df = pd.DataFrame(raw, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_volume", "trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)
        return df[["open", "high", "low", "close", "volume"]]
    except Exception as e:
        print(f"[Fetcher] Error Binance: {e}")
        return pd.DataFrame()


def fetch_binance_price(symbol: str = "BTCUSDT") -> float:
    """Harga terkini dari Binance."""
    try:
        base = "https://testnet.binancefuture.com" if config.BINANCE_TESTNET else "https://fapi.binance.com"
        resp = requests.get(f"{base}/fapi/v1/ticker/price", params={"symbol": symbol}, timeout=5)
        return float(resp.json()["price"])
    except Exception as e:
        print(f"[Fetcher] Price error: {e}")
        return 0.0
