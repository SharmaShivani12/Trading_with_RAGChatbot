import os
import pandas as pd
import requests
from datetime import datetime, timedelta

# Directory for historical CSVs
DATA_DIR = "data/prices"

# Map between short symbol and your CSV filenames
COIN_MAP = {
    "btc": "coin_Bitcoin.csv",
    "eth": "coin_Ethereum.csv",
    "ada": "coin_Cardano.csv",
    "ltc": "coin_Litecoin.csv",
    "xrp": "coin_Ripple.csv",
    "dot": "coin_Polkadot.csv",
    "doge": "coin_Dogecoin.csv",
    "sol": "coin_Solana.csv"
}

# CoinGecko IDs for supported coins
COINGECKO_MAP = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "ada": "cardano",
    "ltc": "litecoin",
    "xrp": "ripple",
    "dot": "polkadot",
    "doge": "dogecoin",
    "sol": "solana"
}

# -------------------------
# Load historical CSVs (local fallback)
# -------------------------
def load_crypto_history(symbol: str):
    symbol = symbol.lower()
    if symbol not in COIN_MAP:
        raise ValueError(f"❌ Unknown symbol: {symbol}")

    filepath = os.path.join(DATA_DIR, COIN_MAP[symbol])
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No CSV file found for {symbol} in {DATA_DIR}")

    df = pd.read_csv(filepath)
    df["Date"] = pd.to_datetime(df["Date"])
    return df


# -------------------------
# Get live prices (CoinGecko API)
# -------------------------
def get_latest_price(symbol: str):
    symbol = symbol.lower()
    if symbol not in COINGECKO_MAP:
        raise ValueError(f"❌ Live price not supported for {symbol}")

    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": COINGECKO_MAP[symbol], "vs_currencies": "usd"}

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data[COINGECKO_MAP[symbol]]["usd"]
    except Exception as e:
        print(f"⚠️ API error: {e}")
        # fallback to last close in CSV
        df = load_crypto_history(symbol)
        return df["Close"].iloc[-1]


# -------------------------
# Get historical prices (CoinGecko API)
# -------------------------
def get_historical_prices(symbol: str, days: int = 7):
    """
    Fetch daily closing prices for the last `days` days.
    Falls back to local CSV if API fails.
    """
    symbol = symbol.lower()
    if symbol not in COINGECKO_MAP:
        raise ValueError(f"❌ Historical price not supported for {symbol}")

    url = f"https://api.coingecko.com/api/v3/coins/{COINGECKO_MAP[symbol]}/market_chart"
    params = {"vs_currency": "usd", "days": days}

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # Extract daily closing prices
        prices = [p[1] for p in data["prices"]]  # [timestamp, price]
        return prices
    except Exception as e:
        print(f"⚠️ API error: {e}")
        # fallback to CSV last `days` rows
        df = load_crypto_history(symbol)
        return df["Close"].tail(days).tolist()
