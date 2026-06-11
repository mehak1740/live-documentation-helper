import os
# 1. CRITICAL: Intercept Protocol Buffer descriptor generation before any heavy packages load
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import streamlit as st
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# 2. Load Environment Credentials (Gemini API, LangSmith tracking)
load_dotenv()

# 3. Streamlit Interface Configuration Layout
st.set_page_config(
    page_title="Live Documentation Assistant & Chat Engine",
    page_icon="🌐",
    layout="centered"
)

st.title("🧬 Live Documentation Assistant & Chat Engine")
st.write("Hybrid RAG: Merging Local Vector Memory with Real-Time Web Exploration.")
st.write("---")

# 4. Initialize Core Engine Components (Cached for Performance)
@st.cache_resource
def initialize_rag_components():
    # Production-standard 2026 embeddings string path
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")
    
    # Connect to existing local Chroma DB store
    vector_store = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})
    
    # Initialize Live Search Utility
    search_tool = DuckDuckGoSearchRun()
    
    # Initialize Core LLM Brain
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)
    
    return retriever, search_tool, llm

try:
    retriever, search_tool, llm = initialize_rag_components()
except Exception as e:
    st.error(f"Initialization Error: Ensure your .env keys are valid and ingestion.py was run. Details: {e}")
    st.stop()

# 5. Build the Parallel Hybrid Execution Chain
# Custom system instructions telling the brain how to balance both inputs
# 5. Build the Parallel Hybrid Execution Chain
prompt_template = ChatPromptTemplate.from_template(
    "You are the 'Live Documentation Assistant & Chat Engine', a high-fidelity technical RAG pipeline.\n"
    "CRITICAL ROUTING INSTRUCTION:\n"
    "1. If the user input is a simple greeting (e.g., 'hello', 'hi', 'hey'), small talk, or an generic intro, "
    "respond with a warm, professional welcome. Briefly introduce yourself as a documentation engine and ask how you can help them today. Do NOT force technical context from the database into a simple greeting.\n"
    "2. If the user input is a technical question, synthesize an answer using BOTH the local vector database documentation context AND live web search results. Prioritize verified info from live web search for 2026 data if they conflict.\n\n"
    "--- LOCAL VECTOR CONTEXT ---\n{local_context}\n\n"
    "--- LIVE WEB CONTEXT ---\n{web_context}\n\n"
    "User Question: {question}\n\n"
    "Structured Answer:"
)

# Component formatting wrappers
def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])

def run_web_search(query):
    try:
        return search_tool.run(query)
    except Exception:
        return "Live web search temporarily unavailable or throttled."

# Parallelized pipeline chain maps input to both paths concurrently
hybrid_chain = (
    RunnableParallel(
        {
            "local_context": retriever | format_docs,
            "web_context": RunnablePassthrough() | run_web_search,
            "question": RunnablePassthrough()
        }
    )
    | prompt_template
    | llm
    | StrOutputParser()
)

# 6. Session Chat UI State Tracking
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render ongoing conversation logs
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Accept user inputs
if user_query := st.chat_input("Ask a question (e.g., What is LangSmith Fleet?)"):
    # Display user entry
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Generate response stream
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        with st.spinner("Querying vector indices and scanning live web tracks..."):
            try:
                # Fire the hybrid chain execution map
                answer = hybrid_chain.invoke(user_query)
                response_placeholder.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Execution Error: {e}")