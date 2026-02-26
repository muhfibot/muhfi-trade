# muhfi-trade 📊

Autonomous Futures Trading Bot — BTC/USDT Crypto & Forex (EUR/USD, XAU/USD)

## Features
- Multi-layer analysis: Technical + Fundamental + Sentiment + ML
- Confidence scoring (threshold >90% untuk open posisi)
- Risk management: SL 1-2%, TP 3-5%, max 5% kapital per trade
- Paper trading default, live trading dengan konfirmasi
- News alerts via Telegram
- Backtest engine dengan data historis

## Markets
- **Crypto:** BTC/USDT (Binance Futures)
- **Forex:** EUR/USD, XAU/USD (OANDA)

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env dengan API keys kamu
python main.py
```

## Commands
| Command | Description |
|---------|-------------|
| `/alert on` | Aktifkan news notification |
| `/alert off` | Matikan news notification |
| `/live on` | Switch ke live trading |
| `/paper` | Kembali ke paper trading |
| `/scan BTC` | Analisis BTC/USDT |
| `/scan XAUUSD` | Analisis XAU/USD |
| `/status` | Status bot & posisi aktif |

## Architecture
```
muhfi-trade/
├── main.py              # Entry point
├── config.py            # Konfigurasi & env vars
├── bot/
│   ├── analyzer.py      # Multi-layer analysis engine
│   ├── technical.py     # TA indicators (RSI, MACD, MA, BB)
│   ├── fundamental.py   # News & economic calendar
│   ├── sentiment.py     # Sentiment analysis
│   ├── ml_model.py      # Simple ML (linear regression)
│   ├── confidence.py    # Confidence scoring
│   ├── risk.py          # Risk management
│   └── trader.py        # Order execution
├── data/
│   ├── fetcher.py       # Binance/OANDA data fetcher
│   └── news.py          # News scraper
├── notifications/
│   └── telegram.py      # Telegram alerts
└── tests/
    └── backtest.py      # Backtesting engine
```

## Risk Disclaimer
Bot ini untuk tujuan edukasi. Trading futures mengandung risiko tinggi. Gunakan dengan bijak.
