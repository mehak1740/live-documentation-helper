import streamlit as st
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# Set up clean web page configuration
st.set_page_config(page_title="Live Doc Helper", page_icon="🌐", layout="centered")
st.title("🌐 Live Documentation Assistant")
st.write("Ask any question about fast-changing frameworks, news, or APIs. The agent will check the live web before responding.")

# 1. Initialize our backend tools once (cached for speed)
@st.cache_resource
def initialize_agent():
    search_tool = DuckDuckGoSearchRun()
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)
    
    system_prompt = (
        "You are an advanced live technical documentation assistant.\n"
        "Answer the user's question clearly using the live web search context provided below.\n"
        "If the search context doesn't contain enough details, use your internal knowledge to give an accurate reply, "
        "but mention that you are relying on general training data.\n\n"
        "Live Web Context:\n{context}"
    )
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}"),
    ])
    
    # Construct LCEL pipeline chain
    chain = (
        {
            "context": RunnablePassthrough() | search_tool,
            "question": RunnablePassthrough()
        }
        | prompt_template
        | llm
        | StrOutputParser()
    )
    return chain

live_search_chain = initialize_agent()

# 2. Maintain conversational state history across page reloads
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! What documentation or updates can I search for you today?"}]

# 3. Render old conversation elements back onto the screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle incoming User Input Prompt
if user_query := st.chat_input("Type your question here (e.g., What are the latest updates in LangChain?)"):
    
    # Render user prompt bubble instantly
    st.chat_message("user").markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Trigger live web execution and render streaming typewriter assistant response
    with st.chat_message("assistant"):
        with st.spinner("Searching the live web via DuckDuckGo..."):
            ai_response = live_search_chain.invoke(user_query)
            st.markdown(ai_response)
            
    # Save assistant execution string back to context log
    st.session_state.messages.append({"role": "assistant", "content": ai_response})