# 🌐 Live Documentation Assistant & Chat Engine

**An intelligent, hybrid documentation assistant powered by LangChain and parallel vector exploration**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3%2B-green.svg)](https://langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B.svg)](https://streamlit.io/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-v0.5%2B-orange.svg)](https://www.trychroma.com/)

---

## 🎯 Overview

The **Live Documentation Assistant & Chat Engine** is a sophisticated AI-powered web application designed to serve as a high-fidelity workspace companion. It provides lightning-fast, factual answers to technical queries using advanced Retrieval-Augmented Generation (RAG) techniques, parallelized web expansion loops, and deep observability components.

### ✨ Key Features

* 📚 **Local Vector Store:** High-density indexing and document parsing using `gemini-embedding-2-preview` on top of local ChromaDB storage instances.
* 🌐 **Real-Time Breakout Track:** Dynamic live fallback search queries powered by the DuckDuckGo Search runner network.
* 🔀 **Parallel Execution Pipelines:** Utilizes LangChain Expression Language (LCEL) maps to trigger search networks and document lookups concurrently.
* 💬 **Smart Conversational Routing:** Intuitively distinguishes casual greetings or conversation entries from core technical documentation lookup prompts.
* 🚀 **Observability Built-In:** Real-time token consumption, latency benchmarks, and multi-agent tracing metrics piped instantly to LangSmith.

---

## 🎬 Demo

<div align="center">
  <video src="public/demo.mp4" width="100%" controls muted></video>
</div>

*Interactive dashboard interface showing the Chat Engine fetching and blending data streams concurrently.*

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| 🖥️ **Frontend UI** | Streamlit Framework | Asynchronous, clean chat layout environment |
| 🧠 **AI Orchestration** | LangChain Core (v0.3+) | LCEL parallel execution pipeline binding hooks |
| 📊 **Observability** | LangSmith Dashboard | Advanced runtime analytics and execution logs |
| 🔍 **Vector Storage** | ChromaDB Engine | Fast semantic storage block memory clusters |
| 🤖 **Core Engine LLM** | Gemini 2.5 Flash | Fast model deployment with low temperature limits |
| 🧬 **Embeddings** | gemini-embedding-2-preview | Generates deep multidimensional vector paths |
| 🐍 **Backend Runtime** | Python 3.11 + `uv` toolchain | Isolated dependency builds and deterministic environment locking |

---

## 🚀 System Architecture

The **Live Documentation Assistant & Chat Engine** is built using a decoupled, parallelized asymmetric RAG framework. Instead of a linear retrieval loop, it forks incoming user queries into two separate asynchronous processing tracks to capture both static local parameters and volatile live internet changes.

### 🏛️ Architecture Blueprint & Flow

                 +---------------------------------------+
                 |         Streamlit Front-End           |
                 |  (User inputs question / greeting)    |
                 +-------------------+-------------------+
                                     |
                                     v
                 +-------------------+-------------------+
                 |      LangChain Expression Language    |
                 |         (LCEL Pipeline Router)        |
                 +------------+---------------+----------+
                              |               |
     [ Track A: Local Memory ]|               |[ Track B: Live Internet ]
                              |               |
                              v               v
       +----------------------+------+ +------+----------------------+
       |  gemini-embedding-2-preview | |  DuckDuckGo Search Engine   |
       +--------------+--------------+ +--------------+--------------+
                      |                              |
                      v                              v
       +--------------+--------------+ +--------------+--------------+
       |     ChromaDB Vector Store   | |    Real-Time Web Scraped     |
       |     (Dense Context K=2)     | |      Context / Snippets      |
       +--------------+--------------+ +--------------+--------------+
                      |                              |
                      +---------------+--------------+
                                      |
                                      v  [Merged Context Payloads]
                 +--------------------+------------------+
                 |       System Prompt Engineering       |
                 |    (Routing & Grounding Constraints)  |
                 +--------------------+------------------+
                                      |
                                      v
                 +--------------------+------------------+
                 |         Gemini 2.5 Flash LLM          |
                 |  (Low Latency / Stable Synthesis)     |
                 +--------------------+------------------+
                                      |
                                      v
                 +--------------------+------------------+
                 |    Streamed Output to UI Dashboard    |
                 |      =====> Piped to LangSmith Trace  |
                 +---------------------------------------+

### 🔁 Step-by-Step Pipeline Execution

1. **Intelligent Query Routing:** The text from the Streamlit entry bar hits the LCEL execution engine. If the prompt is a simple greeting (`"hello"`), the router bypasses deep vector/web retrieval loops entirely to issue an instant contextual welcome statement, preventing "over-grounding".
2. **Asynchronous Forking:** When a technical query is detected, LangChain forks the execution tree into a `RunnableParallel` block:
   * **Vector Search:** Converts the text into mathematical arrays via `gemini-embedding-2-preview` and queries your local `chroma_db` folder for the top 2 closest matching text chunks.
   * **Live Exploration:** Simultaneously spins up a DuckDuckGo worker instance to capture the latest information published on the open web.
3. **Synthesis & Evaluation:** Both data streams are joined and compiled into a structured system template. **Gemini 2.5 Flash** processes the consolidated payload at a low temperature setting (`0.1`) to filter out hallucinations and output an objective technical report.
4. **Telemetry Export:** The response streams cleanly back onto your dashboard page while the full processing tree, latency delays, and token metadata metrics are sent asynchronously to **LangSmith** for live observability tracking.

---

## 🚀 Quick Start

### Prerequisites

* Python 3.11 installed via your machine profile layer
* Google AI Studio API access key
* LangSmith platform developer keys

### Installation & Initialization Steps

1. **Clone the repository workspace**
   ```bash
   git clone [https://github.com/your-username/doc-helper-project.git](https://github.com/your-username/doc-helper-project.git)
   cd doc-helper-project

2. **Initialize your dependencies using uv**

   ```bash
   uv python pin 3.11 #(Pin local session execution target runtime)
   uv sync # (Synchronize environment libraries and package states)

3. **Establish your local .env setup mapping parameters**
   Create a .env file right inside your root project folder layout:

   ```bash
    # (Core Gemini Engine)
   GOOGLE_API_KEY="YOUR_GOOGLE_AI_STUDIO_TOKEN"  

   # (Standardized LangSmith Production Telemetry)
   LANGCHAIN_TRACING_V2="true"
   LANGCHAIN_API_KEY="YOUR_LANGSMITH_LSV2_KEY_HERE"
   LANGCHAIN_PROJECT="doc-helper-project"

4. **Populate your local vector memory cache**

   Add your technical notes or updates to sample_docs.txt, then run the ingestion pipeline script:

   ```bash
   uv run python ingestion.py

5. **Fire up the web chat platform workspace**
    
    Navigate your desktop web browser path over to http://localhost:8501 to view your live assistant framework.

   ```bash
   uv run streamlit run app.py

## 🔧 Windows Troubleshooting Note
   ** If your Windows terminal session flags an explicit descriptor compilation error message sequence:
   TypeError: Descriptors cannot be created directly. ** 

   Force your terminal profile instance to utilize pure Python implementations before starting the Streamlit application server block:
   set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
   uv run streamlit run app.py

