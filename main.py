"""
main.py - Entry point muhfi-trade bot
"""
import schedule
import time
import logging
import colorlog
import config
from bot.analyzer import analyze, format_report
from data.news import get_high_impact_news

# === Logging ===
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s[%(levelname)s]%(reset)s %(message)s"
))
log = logging.getLogger("muhfi-trade")
log.addHandler(handler)
log.setLevel(logging.INFO)

# === State ===
state = {
    "mode": config.TRADING_MODE,
    "alerts_on": False,
    "positions": [],
    "last_analysis": {},
}


def run_analysis():
    for symbol in config.CRYPTO_SYMBOLS:
        result = analyze(symbol)
        state["last_analysis"][symbol] = result
        report = format_report(result)
        log.info(f"\n{report}")


def check_news():
    if not state["alerts_on"]:
        return
    for market in ["crypto", "forex"]:
        news = get_high_impact_news(market)
        for article in news[:2]:
            log.warning(f"🔔 Alert: {article['title']}")


def handle_command(cmd: str):
    cmd = cmd.strip().lower()
    if cmd == "/alert on":
        state["alerts_on"] = True
        log.info("✅ News alerts AKTIF")
    elif cmd == "/alert off":
        state["alerts_on"] = False
        log.info("🔕 News alerts MATI")
    elif cmd == "/live on":
        confirm = input("⚠️  Konfirmasi switch ke LIVE trading? (yes/no): ")
        if confirm == "yes":
            state["mode"] = "live"
            log.warning("🔴 Mode: LIVE TRADING")
    elif cmd == "/paper":
        state["mode"] = "paper"
        log.info("📄 Mode: PAPER TRADING")
    elif cmd.startswith("/scan"):
        parts = cmd.split()
        symbol = parts[1].upper() + "USDT" if len(parts) > 1 and not parts[1].upper().endswith("USDT") else (parts[1].upper() if len(parts) > 1 else "BTCUSDT")
        result = analyze(symbol)
        print(format_report(result))
    elif cmd == "/status":
        log.info(f"Mode: {state['mode'].upper()} | Alerts: {state['alerts_on']} | Symbols: {config.CRYPTO_SYMBOLS}")
    else:
        log.info("Commands: /alert on|off | /live on | /paper | /scan <symbol> | /status")


if __name__ == "__main__":
    log.info("🚀 muhfi-trade bot starting...")
    log.info(f"📄 Mode: {config.TRADING_MODE.upper()}")
    log.info(f"📊 Monitoring: {config.CRYPTO_SYMBOLS + config.FOREX_SYMBOLS}")

    schedule.every(config.MONITOR_INTERVAL_SEC).seconds.do(run_analysis)
    schedule.every(config.NEWS_CHECK_INTERVAL_SEC).seconds.do(check_news)

    # Jalankan sekali langsung
    run_analysis()

    log.info("✅ Bot running. Ketik command atau Ctrl+C untuk keluar.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        log.info("Bot stopped.")
