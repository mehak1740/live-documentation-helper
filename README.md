# 🌐 Live Documentation Assistant & Chat Engine

A production-ready, zero-storage **Retrieval-Augmented Generation (RAG)** web application designed to solve the knowledge cutoff problem of standard Large Language Models. Built completely from scratch using **LangChain Expression Language (LCEL)**, powered by **Google Gemini 2.5 Flash**, and integrated with a live **DuckDuckGo Search Engine** wrapper behind a polished, interactive **Streamlit** user interface.

---

## ⚡ Core Engineering Highlights

* **Zero-Storage RAG Architecture:** Eliminates the overhead of complex local or cloud vector databases (like ChromaDB, Pinecone, or pgvector) by dynamically querying and chunking web contexts on the fly.
* **Real-Time Awareness (Pre-grounded Context):** Bypasses standard LLM knowledge limits (allowing precise evaluation of active 2026 technical updates) by executing automated web searches before prompt generation.
* **Failsafe Dual-Engine Logic:** Implements fallback formatting rules via optimized system templates. The assistant explicitly separates verified live web context grounding from its underlying general parametric knowledge base.
* **Production-Grade LCEL Pipeline:** Leverages standard modular operators (`RunnablePassthrough`, `StrOutputParser`) ensuring highly declarative, traceable data flows across asynchronous network sessions.

---

## 🛠️ The Tech Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend Framework** | `Streamlit` | Full-stack interactive reactive chat interface |
| **Pipeline Framework** | `LangChain` | LCEL chain composition & orchestration |
| **Search Infrastructure** | `DuckDuckGo API` | Live web data retrieval without API constraints |
| **Core Brain (LLM)** | `Gemini 2.5 Flash` | Grounded inference, contextual synthesis, & generation |
| **Environment Tooling** | `uv` | Fast virtual environment and dependency provider |

---

## 🧬 Architectural Data Flow
## 🧬 Architectural Data Flow

```mermaid
graph TD
    A[👤 User Input Query] --> B[🎨 Streamlit UI]
    B -->|Captures Session State| C[🔗 LangChain LCEL Pipeline]
    
    C --> D{RunnablePassthrough}
    D -->|Step 1: Execute Search| E[🦆 DuckDuckGo Search Engine]
    D -->|Step 2: Forward Raw Input| F[📝 Original Question]
    
    E -->|Inject Collected Web Snippets| G[⚙️ ChatPromptTemplate System]
    F -->|Inject Context Grounding Rules| G
    
    G --> H[🧠 Gemini 2.5 Flash Model]
    H -->|Generate Response| I[🧩 StrOutputParser]
    I --> J[💬 Live Web Chat Bubble UI]

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style H fill:#f96,stroke:#333,stroke-width:2px
    style J fill:#bfb,stroke:#333,stroke-width:2px
---

🚀 Installation & Local Deployment
Follow these structured steps to set up and run the Live Documentation Assistant on your local machine.

1. Workspace Isolation & Setup
Open your terminal application and change directories into your project folder workspace:
cd doc-helper-project

2. Environment Configuration
Your environment requires a valid Google Gemini API key to interact with the underlying language models. Create a configuration file named .env directly within the root directory:
GOOGLE_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
⚠️ Security Warning: The repository includes a pre-configured .gitignore file. Ensure your .env file remains untracked to prevent leaking sensitive API credentials to public cloud version control managers.

3. Dependency Synchronization
To guarantee a completely isolated and conflict-free execution layer on your machine, run the following optimized uv command. This uses pre-compiled binaries (wheels) to completely bypass local C++ compiler dependencies:
uv pip install langchain-community langchain-google-genai duckduckgo-search python-dotenv ddgs streamlit --only-binary :all:

4. Running the Web Application Core
Launch the Streamlit microservice layer to host the system interface locally:

uv run streamlit run app.py

Once initialized, the terminal window will display your local network addresses, and a clean, responsive development interface will automatically launch in your default web browser at:
http://localhost:8501

🎨 Interactive Preview Check
The system features a structured chat loop history using native container tokens. It manages advanced data extraction pipelines safely:

Streamlined custom user icons tracking live responses.

Active technical updates filtering (e.g., extracting precise LangChain 1.x release properties or custom subagent structures seamlessly from online developer forums).

📜 Repository Structure
doc-helper-project/
├── .env                  # Authenticated secret infrastructure keys (git-ignored)
├── .gitignore            # Version control safety exclusion configurations
├── app.py                # Full-stack Streamlit application interface layout
├── main.py               # Pure core LCEL terminal execution pipeline script
├── pyproject.toml        # Declarative package dependencies metadata manifest
├── README.md             # Professional documentation summary interface
└── uv.lock               # Deterministic locked environment version layout