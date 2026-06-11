import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def main():
    print("--- Initializing Hybrid (ChromaDB Vector Store + Live Search) RAG Agent ---")

    # Fixed: Alignment config to text-embedding-004
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")
    
    if not os.path.exists("./chroma_db"):
        print("⚠️ Warning: './chroma_db' folder not found. Please run 'uv run python ingestion.py' first!")
        return

    vector_store = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    db_retriever = vector_store.as_retriever(search_kwargs={"k": 2})

    search_tool = DuckDuckGoSearchRun()
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)

    system_prompt = (
        "You are an advanced engineering assistant operating with access to hybrid memory banks.\n"
        "Synthesize an accurate response using BOTH database storage context and live web lookups.\n\n"
        "📁 [Database Memory Context]:\n{db_context}\n\n"
        "🌐 [Live Web Search Context]:\n{web_context}\n\n"
        "If the information is missing from both banks, rely on your internal training knowledge but state it clearly."
    )
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}"),
    ])

    hybrid_search_chain = (
        {
            "db_context": db_retriever | format_docs,
            "web_context": RunnablePassthrough() | search_tool,
            "question": RunnablePassthrough()
        }
        | prompt_template
        | llm
        | StrOutputParser()
    )

    user_query = "What is LangSmith Fleet and what are the latest updates in LangChain in 2026?"
    print(f"\n[User Query]: {user_query}")
    print("Querying ChromaDB vector storage and searching live internet simultaneously...\n")

    ai_response = hybrid_search_chain.invoke(user_query)

    print("--- Hybrid Assistant Response ---")
    print(ai_response)

if __name__ == "__main__":
    main()