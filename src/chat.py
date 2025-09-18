import streamlit as st
from market import get_latest_price, load_crypto_history, COIN_MAP
from rag import ask_rag
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Crypto Trading Assistant", layout="wide")

# ---------------- Sidebar (Quick Check) ----------------
st.sidebar.subheader("⚡ Quick Check")
coin = st.sidebar.selectbox("Select a coin", list(COIN_MAP.keys()), key="sidebar_coin")
if st.sidebar.button("Get Latest Price", key="sidebar_price_btn"):
    price = get_latest_price(coin)
    st.sidebar.success(f"💰 {coin.upper()} price: ${price:.2f}")

# ---------------- Main App ----------------
st.title("📊 Crypto Trading Assistant")

st.subheader("💬 Ask the Trading Assistant")

# Multi-line input
user_input = st.text_area("💬 Type your crypto question...", height=100, key="chat_input")

if st.button("Send", key="send_btn") and user_input.strip():
    # 1. Handle "trend" questions (generate chart)
    if "trend" in user_input.lower():
        symbol = None
        for coin_key in COIN_MAP.keys():
            if coin_key in user_input.lower():
                symbol = coin_key
                break
        if not symbol:
            symbol = "btc"

        df = load_crypto_history(symbol)
        chart_path = f"charts/{symbol}_trend.png"

        os.makedirs("charts", exist_ok=True)
        plt.figure(figsize=(8, 4))
        plt.plot(df["Date"].tail(7), df["Close"].tail(7), marker="o", label=f"{symbol.upper()} Price")
        plt.title(f"{symbol.upper()} 7-Day Trend")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.legend()
        plt.grid(True)
        plt.savefig(chart_path)
        plt.close()

        st.info(f"📈 Here’s the 7-day trend for **{symbol.upper()}**.")
        st.image(chart_path)

    # 2. Handle price-related queries
    elif "price" in user_input.lower():
        symbol = None
        for coin_key in COIN_MAP.keys():
            if coin_key in user_input.lower():
                symbol = coin_key
                break
        if not symbol:
            symbol = "btc"

        price = get_latest_price(symbol)
        st.success(f"💰 {symbol.upper()} price is **${price:.2f}**")

    # 3. Handle buy/sell queries (rule-based signals)
    elif "buy" in user_input.lower() or "sell" in user_input.lower():
        symbol = None
        for coin_key in COIN_MAP.keys():
            if coin_key in user_input.lower():
                symbol = coin_key
                break
        if not symbol:
            symbol = "btc"

        if symbol in COIN_MAP:
            # Get latest price
            price = get_latest_price(symbol)

            # Get last 7-day trend
            df = load_crypto_history(symbol)
            last_7 = df.tail(7)
            pct_change = ((last_7["Close"].iloc[-1] - last_7["Close"].iloc[0]) / last_7["Close"].iloc[0]) * 100

            # Simple rule-based recommendation
            if pct_change > 5:
                advice = f"✅ {symbol.upper()} looks bullish ({pct_change:.2f}% in 7 days). Consider **BUYING**."
            elif pct_change < -5:
                advice = f"⚠️ {symbol.upper()} looks bearish ({pct_change:.2f}% in 7 days). Consider **SELLING**."
            else:
                advice = f"🤔 {symbol.upper()} is moving sideways ({pct_change:.2f}% in 7 days). Hold for now."

            # Show results
            st.success(f"💰 Latest {symbol.upper()} price: ${price:.2f}\n\n{advice}")

            # Plot chart
            chart_path = f"charts/{symbol}_signal.png"
            os.makedirs("charts", exist_ok=True)
            plt.figure(figsize=(8, 4))
            plt.plot(last_7["Date"], last_7["Close"], marker="o", color="blue", label=f"{symbol.upper()} Price")
            plt.title(f"{symbol.upper()} - Last 7 Days Trend")
            plt.xlabel("Date")
            plt.ylabel("Price (USD)")
            plt.legend()
            plt.grid(True)
            plt.savefig(chart_path)
            plt.close()

            st.image(chart_path)

        else:
            st.warning("⚠️ Buy/Sell not available for this symbol.")

    # 4. General RAG Q&A
    else:
        response = ask_rag(user_input)
        st.info(response)
