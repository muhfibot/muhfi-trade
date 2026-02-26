"""
bot/analyzer.py - Main analysis engine
Gabungkan: technical + fundamental + sentiment + ML
"""
import pandas as pd
from bot.technical import analyze_technical
from bot.confidence import calc_confidence
from bot.risk import calc_trade_params
from data.fetcher import fetch_binance_klines, fetch_binance_price
from data.news import get_high_impact_news


def simple_sentiment_score(news_items: list) -> float:
    """Hitung sentiment score sederhana dari judul berita (0=bearish, 1=bullish)."""
    if not news_items:
        return 0.5
    bullish_kw = ["rally", "surge", "bullish", "up", "high", "gain", "approve", "etf", "buy"]
    bearish_kw = ["crash", "drop", "bearish", "down", "low", "loss", "ban", "sell", "fear"]
    bull = sum(1 for a in news_items for kw in bullish_kw if kw in a["title"].lower())
    bear = sum(1 for a in news_items for kw in bearish_kw if kw in a["title"].lower())
    total = bull + bear
    if total == 0:
        return 0.5
    return round(bull / total, 3)


def simple_ml_score(df: pd.DataFrame) -> float:
    """Linear regression sederhana untuk prediksi tren (0=down, 1=up)."""
    try:
        from sklearn.linear_model import LinearRegression
        import numpy as np
        y = df["close"].values[-50:]
        x = np.arange(len(y)).reshape(-1, 1)
        model = LinearRegression().fit(x, y)
        slope = model.coef_[0]
        # Normalize: positif slope = bullish
        max_slope = df["close"].std()
        score = 0.5 + (slope / (2 * max_slope + 1e-9)) * 0.5
        return round(max(0.0, min(1.0, score)), 3)
    except Exception:
        return 0.5


def analyze(symbol: str = "BTCUSDT", capital: float = 1000.0) -> dict:
    """Full multi-layer analysis untuk satu simbol."""
    print(f"[Analyzer] Analyzing {symbol}...")

    # 1. Fetch data
    df = fetch_binance_klines(symbol, interval="1h", limit=300)
    if df.empty:
        return {"error": f"Tidak bisa fetch data untuk {symbol}"}

    price = fetch_binance_price(symbol) or df["close"].iloc[-1]

    # 2. Technical analysis (40%)
    tech = analyze_technical(df)
    tech_score = tech["score"]

    # 3. News & fundamental (25%)
    news = get_high_impact_news("crypto")
    fund_score = 0.5  # default neutral
    if news:
        # Ada high-impact news → slight boost atau bearish tergantung sentimen
        fund_score = simple_sentiment_score(news)

    # 4. Sentiment (25%)
    all_news = news  # bisa diperluas dengan X/Reddit scrape
    sent_score = simple_sentiment_score(all_news) if all_news else 0.5

    # 5. ML (10%)
    ml_score = simple_ml_score(df)

    # 6. Confidence
    conf = calc_confidence(tech_score, fund_score, sent_score, ml_score)
    direction = tech["direction"]

    # 7. Risk params
    risk = calc_trade_params(price, direction, capital)

    result = {
        "symbol": symbol,
        "price": price,
        "direction": direction,
        "confidence": conf,
        "technical": tech,
        "fundamental": {"score": fund_score, "news_count": len(news), "top_news": [n["title"] for n in news[:3]]},
        "sentiment": {"score": sent_score},
        "ml": {"score": ml_score},
        "trade": risk if conf["threshold_met"] else None,
        "recommendation": "OPEN POSITION ✅" if conf["threshold_met"] else f"WAIT — confidence {conf['confidence_pct']} < 90%",
    }
    return result


def format_report(result: dict) -> str:
    """Format hasil analisis jadi pesan Telegram."""
    if "error" in result:
        return f"❌ Error: {result['error']}"

    conf = result["confidence"]
    tech = result["technical"]
    fund = result["fundamental"]
    r = result.get("trade")

    msg = f"""📊 *Analisis {result['symbol']}*
💰 Harga: `{result['price']}`
📈 Arah: `{result['direction'].upper()}`
🎯 Confidence: `{conf['confidence_pct']}`

*Technical (40%)*
• RSI: {tech['rsi']} | MACD hist: {tech['macd_histogram']}
• MA50: {tech['ma50']} | MA200: {tech['ma200']}
• BB: {tech['bb_lower']} — {tech['bb_upper']}
• Sinyal: {', '.join(tech['signals']) or 'Neutral'}

*Fundamental (25%)*
• Score: {fund['score']} | News: {fund['news_count']} high-impact
{chr(10).join('• ' + n for n in fund['top_news']) if fund['top_news'] else '• Tidak ada news signifikan'}

*Confidence Breakdown*
{chr(10).join('• ' + v for v in conf['breakdown'].values())}

*Rekomendasi*
{result['recommendation']}"""

    if r:
        msg += f"""

📋 *Trade Setup*
Entry: `{r['entry']}`
SL: `{r['sl']}` ({r['sl_pct']})
TP: `{r['tp']}` ({r['tp_pct']})
R:R = {r['rr_ratio']}
Position: `${r['position_value_usd']}` (5% kapital)
Risk: `${r['risk_usd']}` | Reward: `${r['reward_usd']}`"""

    return msg
