"""
bot/risk.py - Risk Management
SL 1-2%, TP 3-5%, max 5% kapital per trade
"""
from config import STOP_LOSS_PCT, TAKE_PROFIT_PCT, MAX_POSITION_SIZE


def calc_trade_params(entry_price: float, direction: str, capital: float = 1000.0) -> dict:
    """
    Hitung SL, TP, dan position size.
    direction: 'long' atau 'short'
    """
    if direction == "long":
        sl = round(entry_price * (1 - STOP_LOSS_PCT), 4)
        tp = round(entry_price * (1 + TAKE_PROFIT_PCT), 4)
    else:
        sl = round(entry_price * (1 + STOP_LOSS_PCT), 4)
        tp = round(entry_price * (1 - TAKE_PROFIT_PCT), 4)

    position_value = capital * MAX_POSITION_SIZE
    qty = round(position_value / entry_price, 6)
    risk_amount = round(position_value * STOP_LOSS_PCT, 2)
    reward_amount = round(position_value * TAKE_PROFIT_PCT, 2)
    rr_ratio = round(TAKE_PROFIT_PCT / STOP_LOSS_PCT, 1)

    return {
        "entry": entry_price,
        "sl": sl,
        "tp": tp,
        "direction": direction,
        "position_value_usd": round(position_value, 2),
        "qty": qty,
        "risk_usd": risk_amount,
        "reward_usd": reward_amount,
        "rr_ratio": f"1:{rr_ratio}",
        "sl_pct": f"{STOP_LOSS_PCT*100}%",
        "tp_pct": f"{TAKE_PROFIT_PCT*100}%",
    }
