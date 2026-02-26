"""
Realtime Price Monitor for Neo
Monitors Bitcoin price in real-time and sends alerts to Neo
"""

import requests
import time
import json
import os

# Configuration
BITCOIN_SETUP = {
    "entry": 69000.0,
    "sl": 68000.0,
    "tp1": 70500.0,
    "tp2": 72000.0,
    "position_size": 0.02  # 2% of capital
}

# API Endpoints
COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true&include_market_cap=true&include_24hr_vol=true"

# Neo's alert endpoint (replace with actual)
NEO_ALERT_ENDPOINT = "https://api.neo-bot.com/alerts"

# API Key (if required)
API_KEY = os.getenv("COINGECKO_API_KEY", None)

# Headers
HEADERS = {
    "User-Agent": "Neo-Price-Monitor/1.0",
    "Accept": "application/json"
}

if API_KEY:
    HEADERS["Authorization"] = f"Bearer {API_KEY}"

def fetch_bitcoin_price():
    """Fetch real-time Bitcoin price from CoinGecko API"""
    try:
        response = requests.get(COINGECKO_API, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        price = data["bitcoin"]["usd"]
        change = data["bitcoin"]["usd_24h_change"]
        market_cap = data["bitcoin"]["usd_market_cap"]
        volume = data["bitcoin"]["usd_24h_vol"]
        
        return {
            "price": price,
            "change": change,
            "market_cap": market_cap,
            "volume": volume,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        print(f"Error fetching Bitcoin price: {e}")
        return None

def send_alert(message):
    """Send alert to Neo"""
    try:
        payload = {
            "message": message,
            "source": "Neo-Price-Monitor",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # For now, just print the alert
        print(f"ALERT: {message}")
        
        # Uncomment to send actual alerts
        # response = requests.post(NEO_ALERT_ENDPOINT, json=payload, headers=HEADERS)
        # response.raise_for_status()
        
    except Exception as e:
        print(f"Error sending alert: {e}")

def check_setup_triggers(price):
    """Check if setup triggers are met"""
    entry = BITCOIN_SETUP["entry"]
    sl = BITCOIN_SETUP["sl"]
    tp1 = BITCOIN_SETUP["tp1"]
    tp2 = BITCOIN_SETUP["tp2"]
    
    # Check for entry trigger
    if price >= entry:
        send_alert(f"🚨 BTC SETUP TRIGGERED!
Price: ${price:,.2f}
Setup: Entry ${entry:,.2f} / SL ${sl:,.2f} / TP1 ${tp1:,.2f} / TP2 ${tp2:,.2f}
Action: OPEN LONG @ ${price:,.2f}")
        return True
    
    # Check for stop loss
    if price <= sl:
        send_alert(f"⚠️ BTC STOP LOSS HIT!
Price: ${price:,.2f}
SL: ${sl:,.2f}
Action: CLOSE POSITION")
        return True
    
    # Check for take profits
    if price >= tp1:
        send_alert(f"✅ BTC TAKE PROFIT 1!
Price: ${price:,.2f}
TP1: ${tp1:,.2f}
Action: CLOSE 50% POSITION")
        return True
    
    if price >= tp2:
        send_alert(f"🎉 BTC TAKE PROFIT 2!
Price: ${price:,.2f}
TP2: ${tp2:,.2f}
Action: CLOSE REMAINING POSITION")
        return True
    
    return False

def monitor_bitcoin_price():
    """Main monitoring loop"""
    print("Neo Price Monitor Started")
    print("Monitoring Bitcoin price in real-time...")
    print("Press Ctrl+C to stop")
    
    while True:
        try:
            # Fetch real-time price
            data = fetch_bitcoin_price()
            
            if data:
                price = data["price"]
                change = data["change"]
                market_cap = data["market_cap"]
                volume = data["volume"]
                timestamp = data["timestamp"]
                
                # Display price information
                print(f"\n{time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Bitcoin Price: ${price:,.2f}")
                print(f"24h Change: {change:+.2f}%")
                print(f"Market Cap: ${market_cap/1e9:.2f}B")
                print(f"24h Volume: ${volume/1e9:.2f}B")
                
                # Check for setup triggers
                check_setup_triggers(price)
                
                # Save to log file
                with open("bitcoin_price_log.txt", "a") as f:
                    f.write(f"{timestamp}, {price:.2f}, {change:.2f}, {market_cap}, {volume}\n")
            
            # Wait before next check
            time.sleep(60)  # Check every 60 seconds
            
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
            break
        except Exception as e:
            print(f"Error in monitoring loop: {e}")
            time.sleep(60)

if __name__ == "__main__":
    monitor_bitcoin_price()