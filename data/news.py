"""
data/news.py - News scraper (Coingecko, Investing.com RSS, Forex Factory)
"""
import feedparser
import requests
from datetime import datetime


FEEDS = {
    "crypto": [
        "https://www.coindesk.com/arc/outboundfeeds/rss/",
        "https://cointelegraph.com/rss",
    ],
    "forex": [
        "https://www.forexlive.com/feed/news",
        "https://www.investing.com/rss/news_25.rss",
    ]
}

HIGH_IMPACT_KEYWORDS = [
    "fed", "rate", "inflation", "cpi", "nfp", "fomc", "powell",
    "halving", "etf", "sec", "regulation", "ban", "crash", "rally",
    "gdp", "unemployment", "ecb", "boj"
]


def fetch_news(market: str = "crypto", limit: int = 10) -> list:
    """Ambil berita terbaru dari RSS feeds."""
    articles = []
    feeds = FEEDS.get(market, FEEDS["crypto"])
    for feed_url in feeds:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:limit]:
                articles.append({
                    "title": entry.get("title", ""),
                    "summary": entry.get("summary", "")[:300],
                    "link": entry.get("link", ""),
                    "published": entry.get("published", str(datetime.now())),
                    "source": feed_url,
                })
        except Exception as e:
            print(f"[News] Feed error {feed_url}: {e}")
    return articles


def is_high_impact(title: str) -> bool:
    """Cek apakah berita high-impact."""
    title_lower = title.lower()
    return any(kw in title_lower for kw in HIGH_IMPACT_KEYWORDS)


def get_high_impact_news(market: str = "crypto") -> list:
    """Filter hanya berita high-impact."""
    articles = fetch_news(market)
    return [a for a in articles if is_high_impact(a["title"])]
