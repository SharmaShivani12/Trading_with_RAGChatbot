import streamlit as st
from market import get_latest_price, load_crypto_history, COIN_MAP
from bot import master_chatbot
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
    user_input_lower = user_input.lower()

    # Helper: extract symbol from user input
    def extract_symbol(text: str):
        words = text.lower().split()
        for w in words:
            if w in COIN_MAP:
                return w
        return "btc"  # fallback

    # 1. Handle "trend" questions (generate chart)
    if "trend" in user_input_lower:
        symbol = extract_symbol(user_input_lower)
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
    elif "price" in user_input_lower:
        symbol = extract_symbol(user_input_lower)
        price = get_latest_price(symbol)
        st.success(f"💰 {symbol.upper()} price is **${price:.2f}**")

    # 3. Handle buy/sell queries with RAG
    elif "buy" in user_input_lower or "sell" in user_input_lower:
        response = ask_rag(user_input)
        st.success(response)

    else:
        # General RAG Q&A
        response = ask_rag(user_input)
        st.info(response)
