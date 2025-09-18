from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

import os

def build_vectorstore(data_path="data/research", db_path="vectorstore"):
    # 1. Load all PDFs from folder
    loader = DirectoryLoader(data_path, glob="**/*.pdf", loader_cls=PyPDFLoader)
    docs = loader.load()
    print(f"✅ Loaded {len(docs)} pages from PDFs in {data_path}")

    # 2. Split into smaller chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    print(f"✅ Split into {len(chunks)} chunks")

    # 3. Convert text into embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 4. Build FAISS vector store
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # 5. Save the vectorstore locally
    os.makedirs(db_path, exist_ok=True)
    vectorstore.save_local(db_path)
    print(f"✅ Vectorstore saved at {db_path}")


if __name__ == "__main__":
    build_vectorstore()
