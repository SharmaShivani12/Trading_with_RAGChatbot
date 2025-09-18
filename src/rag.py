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

# -----------------------------
# Ask RAG with Ollama directly
# -----------------------------
def ask_rag(query: str) -> str:
    try:
        # 1. Retrieve top docs from FAISS
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        docs = retriever.get_relevant_documents(query)
        context = "\n\n".join([doc.page_content for doc in docs])

        # 2. Construct prompt
        prompt = f"""
You are a helpful crypto trading assistant.
Use the context below to answer the question clearly and concisely.
If the context is not useful, answer from your trading knowledge.
If you don’t know, just say: "⚠️ Sorry, I don’t have info on that."

Context:
{context}

Question: {query}

Answer:
"""

        # 3. Call Ollama (small CPU-friendly model)
        response = ollama.chat(
            model="gemma:2b",   # or "phi:2.7b", whichever you pulled
            messages=[{"role": "user", "content": prompt}]
        )

        return response["message"]["content"].strip()

    except Exception as e:
        return f"⚠️ Error while searching research docs: {str(e)}"
