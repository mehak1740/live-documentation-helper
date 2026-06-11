import os
# Force the Protocol Buffers implementation BEFORE importing anything else
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

def load_and_index_docs():
    print("--- Initializing Documentation Ingestion Flow ---")
    
    sample_doc_path = "sample_docs.txt"
    if not os.path.exists(sample_doc_path):
        with open(sample_doc_path, "w", encoding="utf-8") as f:
            f.write(
                "LangChain v1.0 was released in late 2025, moving core components to stable lines.\n"
                "LangSmith Fleet is a 2026 enterprise management system for monitoring multi-agent clusters.\n"
                "ChromaDB serves as an open-source vector store designed specifically for AI agent memory systems."
            )
        print(f"Created a sample knowledge file: {sample_doc_path}")

    loader = TextLoader(sample_doc_path, encoding="utf-8")
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=30)
    docs = text_splitter.split_documents(documents)
    print(f"Split source files into {len(docs)} chunks.")

    # Using the production-standard preview string for the 2026 LangChain package layout
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")

    persist_directory = "./chroma_db"
    print(f"Saving vector indices locally inside '{persist_directory}'...")
    
    Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    print("--- Local Database Ingestion Complete! ---")

if __name__ == "__main__":
    load_and_index_docs()