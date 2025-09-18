from market import get_latest_price, load_crypto_history
import matplotlib.pyplot as plt
import os
from market import get_latest_price, COIN_MAP
from rag import ask_rag


def master_chatbot(query: str):
    query = query.lower()

    # Handle price queries
    for coin in ["btc", "eth", "ada", "ltc", "xrp", "dot", "doge", "sol"]:
        if coin in query and "price" in query:
            price = get_latest_price(coin)
            return f"💰 The latest price of **{coin.upper()}** is ${price:.2f}"

        if coin in query and "trend" in query:
            df = load_crypto_history(coin)
            last7 = df.tail(7)

            os.makedirs("charts", exist_ok=True)
            chart_path = f"charts/{coin}_trend.png"

            plt.figure(figsize=(6,4))
            plt.plot(last7["Date"], last7["Close"], marker="o", label=f"{coin.upper()} Price")
            plt.title(f"{coin.upper()} - 7 Day Trend")
            plt.xlabel("Date")
            plt.ylabel("USD")
            plt.legend()
            plt.grid(True)
            plt.savefig(chart_path)
            plt.close()

            return (f"📈 Here’s the 7-day trend for **{coin.upper()}**.", chart_path)

    return "🤖 I can answer questions about crypto prices and trends (BTC, ETH, ADA, etc.)."
