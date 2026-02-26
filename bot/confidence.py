"""
bot/confidence.py - Confidence scoring engine
Weights: 40% technical, 25% fundamental, 25% sentiment, 10% ML
"""
from config import WEIGHT_TECHNICAL, WEIGHT_FUNDAMENTAL, WEIGHT_SENTIMENT, WEIGHT_ML, CONFIDENCE_THRESHOLD


def calc_confidence(tech_score: float, fund_score: float, sent_score: float, ml_score: float) -> dict:
    """
    Hitung confidence score dari semua layer.
    Semua score dalam range 0.0 - 1.0
    """
    weighted = (
        tech_score * WEIGHT_TECHNICAL +
        fund_score * WEIGHT_FUNDAMENTAL +
        sent_score * WEIGHT_SENTIMENT +
        ml_score * WEIGHT_ML
    )
    confidence = round(weighted, 4)
    threshold_met = confidence >= CONFIDENCE_THRESHOLD

    return {
        "confidence": confidence,
        "confidence_pct": f"{confidence*100:.1f}%",
        "threshold_met": threshold_met,
        "breakdown": {
            "technical": f"{tech_score:.2f} × {WEIGHT_TECHNICAL} = {tech_score*WEIGHT_TECHNICAL:.3f}",
            "fundamental": f"{fund_score:.2f} × {WEIGHT_FUNDAMENTAL} = {fund_score*WEIGHT_FUNDAMENTAL:.3f}",
            "sentiment": f"{sent_score:.2f} × {WEIGHT_SENTIMENT} = {sent_score*WEIGHT_SENTIMENT:.3f}",
            "ml": f"{ml_score:.2f} × {WEIGHT_ML} = {ml_score*WEIGHT_ML:.3f}",
        }
    }
