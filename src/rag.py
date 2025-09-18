import ollama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# -----------------------------
# Load vectorstore (PDF embeddings)
# -----------------------------
VECTORSTORE_PATH = "vectorstore"

def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.load_local(VECTORSTORE_PATH, embeddings, allow_dangerous_deserialization=True)

vectorstore = load_vectorstore()

from market import get_latest_price, load_crypto_history
import pandas as pd

def ask_rag(query: str):
    query_lower = query.lower()
    response_context = ""

    # --- Price injection ---
    for symbol in ["btc", "eth", "ada", "ltc", "xrp", "dot", "doge", "sol"]:
        if symbol in query_lower:
            # get live price
            price = get_latest_price(symbol)
            response_context += f"\nCurrent {symbol.upper()} price: ${price:.2f}"

            # get last 7-day trend
            df = load_crypto_history(symbol)
            last_7 = df.tail(7)
            pct_change = ((last_7["Close"].iloc[-1] - last_7["Close"].iloc[0]) / last_7["Close"].iloc[0]) * 100
            trend = "uptrend 📈" if pct_change > 0 else "downtrend 📉"
            response_context += f"\n7-day change: {pct_change:.2f}% ({trend})"

            break  # stop after first match

    # --- Feed into your LLM (Ollama / LangChain pipeline) ---
    # Instead of just raw query, prepend data
    prompt = f"User asked: {query}\nHere is some market context:\n{response_context}\nAnswer clearly and short."
    
    # call your chatbot here
    from bot import master_chatbot
    answer = master_chatbot(prompt)
    return answer

