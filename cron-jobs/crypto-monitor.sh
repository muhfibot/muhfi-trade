#!/bin/bash

# Crypto Market Monitor Script
# Runs every 30 minutes to fetch real-time prices and analyze trading setups

# Configuration
LOG_FILE="/root/.openclaw/workspace/muhfi-trade/cron-jobs/crypto-monitor.log"
DATA_FILE="/root/.openclaw/workspace/muhfi-trade/cron-jobs/crypto-data.json"
ALERT_FILE="/root/.openclaw/workspace/muhfi-trade/cron-jobs/alerts.txt"

# Setup Parameters
BTC_ENTRY=69000
BTC_SL=68000
BTC_TP1=70500
BTC_TP2=72000

ETH_BREAKOUT=2320

# API Endpoint
API_URL="https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true&include_market_cap=true&include_24h_vol=true"

# Function to fetch real-time prices
fetch_prices() {
    echo "Fetching real-time crypto prices..."
    response=$(curl -s "$API_URL")
    echo "$response" > "$DATA_FILE"
    echo "Prices fetched successfully"
}

# Function to analyze Bitcoin setup
analyze_btc() {
    echo "Analyzing Bitcoin setup..."
    
    # Extract Bitcoin data
    btc_price=$(echo "$response" | jq -r '.bitcoin.usd')
    btc_change=$(echo "$response" | jq -r '.bitcoin.usd_24h_change')
    
    # Technical Analysis
    echo "BTC Technical Analysis:"
    echo "Current Price: $$btc_price"
    echo "24h Change: $$btc_change%"
    
    # Check for setup triggers
    if [ $(echo "$btc_price >= $BTC_ENTRY" | bc -l) -eq 1 ]; then
        echo "BTC SETUP TRIGGERED!" >> "$ALERT_FILE"
        echo "Entry Price: $$btc_price" >> "$ALERT_FILE"
        echo "Setup: Entry $$BTC_ENTRY / SL $$BTC_SL / TP1 $$BTC_TP1 / TP2 $$BTC_TP2" >> "$ALERT_FILE"
        echo "Action: OPEN LONG POSITION" >> "$ALERT_FILE"
        echo "" >> "$ALERT_FILE"
    fi
}

# Function to analyze Ethereum setup
analyze_eth() {
    echo "Analyzing Ethereum setup..."
    
    # Extract Ethereum data
    eth_price=$(echo "$response" | jq -r '.ethereum.usd')
    eth_change=$(echo "$response" | jq -r '.ethereum.usd_24h_change')
    
    # Technical Analysis
    echo "ETH Technical Analysis:"
    echo "Current Price: $$eth_price"
    echo "24h Change: $$eth_change%"
    
    # Check for breakout
    if [ $(echo "$eth_price >= $ETH_BREAKOUT" | bc -l) -eq 1 ]; then
        echo "ETH BREAKOUT DETECTED!" >> "$ALERT_FILE"
        echo "Breakout Price: $$eth_price" >> "$ALERT_FILE"
        echo "Action: CONSIDER LONG POSITION" >> "$ALERT_FILE"
        echo "" >> "$ALERT_FILE"
    fi
}

# Main execution
main() {
    echo "=== Crypto Market Monitor ===" > "$LOG_FILE"
    echo "Timestamp: $(date)" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
    
    # Fetch prices
    fetch_prices
    
    # Read data
    response=$(cat "$DATA_FILE")
    
    # Analyze setups
    analyze_btc
    analyze_eth
    
    # Log results
    echo "Analysis completed at $(date)" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
    
    # Send alerts if any
    if [ -s "$ALERT_FILE" ]; then
        echo "ALERTS DETECTED:"
        cat "$ALERT_FILE"
        # Clear alert file after sending
        > "$ALERT_FILE"
    else
        echo "No alerts generated"
    fi
    
    echo "Monitor completed"
}

# Execute main function
main "$@"