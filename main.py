import os
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# Load your Gemini API key from the local .env file
load_dotenv()

def main():
    print("--- Initializing Live Web Search RAG Agent ---")

    # 1. Initialize the Free DuckDuckGo Search Engine Tool
    search_tool = DuckDuckGoSearchRun()

    # 2. Connect to the free Gemini cloud intelligence
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)

    # 3. Create an optimized prompt template for live data grounding
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

    # 4. Construct the LCEL Live Search Chain
    live_search_chain = (
        {
            "context": RunnablePassthrough() | search_tool,
            "question": RunnablePassthrough()
        }
        | prompt_template
        | llm
        | StrOutputParser()
    )

    # 5. Execute a live query!
    user_query = "What are the latest updates or release features in LangChain in 2026?"
    print(f"\n[User Query]: {user_query}")
    print("Searching the live internet via DuckDuckGo and compiling answers...\n")

    ai_response = live_search_chain.invoke(user_query)

    print("--- Live Web Assistant Response ---")
    print(ai_response)

if __name__ == "__main__":
    main()