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
    # Production-standard embeddings string path
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")
    
    # Connect to existing local Chroma DB store
    vector_store = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})
    
    # OPTIMIZATION: Set a strict 2-second timeout on the web tool so it never hangs your app
    search_tool = DuckDuckGoSearchRun(timeout=2)
    
    # Initialize Core LLM Brain
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)
    
    return retriever, search_tool, llm

try:
    retriever, search_tool, llm = initialize_rag_components()
except Exception as e:
    st.error(f"Initialization Error: Ensure your .env keys are valid and ingestion.py was run. Details: {e}")
    st.stop()

# 5. Build the Highly Optimized Parallel Hybrid Execution Chain
prompt_template = ChatPromptTemplate.from_template(
    "You are the 'Live Documentation Assistant & Chat Engine', a high-fidelity technical RAG pipeline.\n"
    "Synthesize a crisp, highly direct answer using the provided context.\n"
    "CRITICAL SPEED CONSTRAINT: Be extremely concise. Limit your answer to bullet points and under 120 words total. Do not waste sentences repeating the question.\n\n"
    "--- LOCAL VECTOR CONTEXT ---\n{local_context}\n\n"
    "--- LIVE WEB CONTEXT ---\n{web_context}\n\n"
    "User Question: {question}\n\n"
    "Structured Answer:"
)

# Component formatting wrappers
def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])

# OPTIMIZATION: Smart Router that skips the 4-second web crawl if the question is purely local
# FIX: Dynamically unwraps dictionary structures from LCEL streaming pipelines safely
def smart_web_routing(payload):
    # If LangChain formats the pipeline input as a dictionary, parse out the target key string
    if isinstance(payload, dict) and "question" in payload:
        question_str = payload["question"]
    else:
        question_str = str(payload)
        
    question_lower = question_str.lower()
    local_keywords = ["our", "my", "doc", "documentation", "this project", "local", "sample_docs"]
    
    # If it's asking about local files, skip the internet entirely
    if any(keyword in question_lower for keyword in local_keywords):
        return "Purely local query detected. Skipped web exploration track to optimize latency."
    
    try:
        return search_tool.run(question_str)
    except Exception:
        return "Live web search temporarily unavailable or timed out."

# Parallelized pipeline chain maps input to both paths concurrently
hybrid_chain = (
    RunnableParallel(
        {
            "local_context": retriever | format_docs,
            "web_context": smart_web_routing,  # Uses the updated smart routing logic wrapper
            "question": RunnablePassthrough()
        }
    )
    | prompt_template
    | llm
    | StrOutputParser()
)

# Simple greeting fallback to prevent hitting databases unnecessarily
GREETINGS = {"hello", "hi", "hey", "good morning", "good afternoon", "yo"}

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
        full_response = ""
        
        # OPTIMIZATION: Short-circuit routing for greetings (instantaneous response)
        if user_query.strip().lower().rstrip("!?") in GREETINGS:
            full_response = "Hello! 👋 Welcome to the Live Documentation Assistant. How can I help you navigate your technical documentation or explore live web updates today?"
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        else:
            # OPTIMIZATION: Real-time chunk streaming via .stream() instead of .invoke()
            with st.spinner("Analyzing indices and searching live web tracks..."):
                try:
                    # Fire the hybrid chain chunk generator loop
                    for chunk in hybrid_chain.stream(user_query):
                        full_response += chunk
                        # Append a typing cursor symbol for smooth UI feedback
                        response_placeholder.markdown(full_response + "▌")
                    
                    # Strip out typing cursor when complete
                    response_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    st.error(f"Execution Error: {e}")