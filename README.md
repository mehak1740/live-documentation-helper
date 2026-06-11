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
[ User Query ]
│
▼
┌──────────────┐
│  Streamlit   │ ──► Triggers Reactive Spinner / Session State Capture
└──────────────┘
│
▼
┌──────────────┐
│  LangChain   │ ──► Maps inputs using RunnablePassthrough
└──────────────┘
│
├──────────────────────────────┐
▼                              ▼
┌──────────────┐              ┌──────────────┐
│ DuckDuckGo   │              │ Raw Question │
│ Search Tool  │              └──────────────┘
└──────────────┘                     │
│ (Fetches snippets)           │
▼                              ▼
┌────────────────────────────────────────────┐
│            ChatPromptTemplate              │ ──► Strict grounding instructions inject context
└────────────────────────────────────────────┘
│
▼
┌────────────────────────────────────────────┐
│        Gemini 2.5 Flash Inference          │
└────────────────────────────────────────────┘
│
▼
┌────────────────────────────────────────────┐
│             StrOutputParser                │
└────────────────────────────────────────────┘
│
▼
[ Polished Markdown Web Bubble UI ]


---

## 🚀 Installation & Local Deployment

Follow these complete, isolated setup instructions to execute the workspace on your machine:

### 1. Initialize and Navigate to Workspace
```dos
cd doc-helper-project

2. Configure Environment Parameters
Create a secure credentials file named .env in the root folder directory and attach your Google AI Studio API key:

GOOGLE_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
Note: The local .gitignore is pre-configured to ensure this token is completely isolated and protected from public version control leakage.

3. Deploy Local Package Bindings
Execute standard explicit pre-compiled binary synchronization using the fast uv pip utility to guarantee a conflict-free assembly layer:

uv pip install langchain-community langchain-google-genai duckduckgo-search python-dotenv ddgs streamlit --only-binary :all:

4. Launch the Web Application Server
Fire up the microservice orchestration module:

uv run streamlit run app.py
A reactive development browser port will instantly surface automatically at http://localhost:8501.

🎨 Interactive Preview Check
The system features a structured chat loop history using native container tokens. It manages advanced data extraction pipelines safely:

Streamlined custom user icons tracking live responses.

Active technical updates filtering (e.g., extracting precise LangChain 1.x release properties or custom subagent structures seamlessly from online developer forums).

📜 Repository Structure
Plaintext
doc-helper-project/
├── .env                  # Authenticated secret infrastructure keys (git-ignored)
├── .gitignore            # Version control safety exclusion configurations
├── app.py                # Full-stack Streamlit application interface layout
├── main.py               # Pure core LCEL terminal execution pipeline script
├── pyproject.toml        # Declarative package dependencies metadata manifest
├── README.md             # Professional documentation summary interface
└── uv.lock               # Deterministic locked environment version layout

