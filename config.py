"""
config.py - Konfigurasi & env vars
"""
import os
from dotenv import load_dotenv

load_dotenv()

# === API Keys ===
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY", "")
BINANCE_TESTNET = os.getenv("BINANCE_TESTNET", "true").lower() == "true"

OANDA_API_KEY = os.getenv("OANDA_API_KEY", "")
OANDA_ACCOUNT_ID = os.getenv("OANDA_ACCOUNT_ID", "")
OANDA_ENVIRONMENT = os.getenv("OANDA_ENVIRONMENT", "practice")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# === Trading Mode ===
TRADING_MODE = os.getenv("TRADING_MODE", "paper")  # paper | live

# === Risk Management ===
MAX_POSITION_SIZE = float(os.getenv("MAX_POSITION_SIZE", "0.05"))   # 5%
STOP_LOSS_PCT = float(os.getenv("STOP_LOSS_PCT", "0.02"))           # 2%
TAKE_PROFIT_PCT = float(os.getenv("TAKE_PROFIT_PCT", "0.04"))       # 4%
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.90"))  # 90%

# === Analysis Weights ===
WEIGHT_TECHNICAL = 0.40
WEIGHT_FUNDAMENTAL = 0.25
WEIGHT_SENTIMENT = 0.25
WEIGHT_ML = 0.10

# === Monitored Markets ===
CRYPTO_SYMBOLS = ["BTCUSDT"]
FOREX_SYMBOLS = ["EUR_USD", "XAU_USD"]

# === Intervals ===
MONITOR_INTERVAL_SEC = 900    # 15 menit
NEWS_CHECK_INTERVAL_SEC = 300  # 5 menit

# === TA Parameters ===
RSI_PERIOD = 14
MA_SHORT = 50
MA_LONG = 200
BB_PERIOD = 20
BB_STD = 2
