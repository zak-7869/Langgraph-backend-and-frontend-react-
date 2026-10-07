###System Architecture Diagram
```
       +--------------------------------------------------------+

       |                  CLIENT LAYER (React)                  |
       |  [User Input Form] ---> (POST /api/research)           |
       +----------------------------+---------------------------+
                                    |
                                    | REST HTTP / JSON
                                    v
       +--------------------------------------------------------+

       |                 ROUTING LAYER (Vercel)                 |
       |  Rewrites /api/(.*)   --->  backend/main.py             |
       +----------------------------+---------------------------+
                                    |
                                    | Serverless Function Invoke
                                    v
       +--------------------------------------------------------+

       |                BACKEND LAYER (FastAPI)                 |
       |  Validates Request -> Pydantic Schema                  |
       +----------------------------+---------------------------+
                                    |
                                    v
+----------------------------------------------------------------------+

|                    LANGGRAPH WORKFLOW ENGINE                         |
|                                                                      |
|     +-------------------------+                                      |
|     |    START (Entrypoint)   |                                      |
|     +------------+------------+                                      |
|                  |                                                   |
|                  v                                                   |
|     +-------------------------+       Web Queries     +-----------+  |
|     |     RESEARCHER NODE     |---------------------->| DuckDuckGo|  |
|     |  - Gathers Fact Data     |<----------------------| Search Tool| |
|     |  - Extracts Statistics  |   Aggregated Context  +-----------+  |
|     +------------+------------+                                      |
|                  |                                                   |
|                  | State Transmit: {"research_notes": "..."}         |
|                  v                                                   |
|     +-------------------------+                                      |
|     |      REPORTER NODE      |                                      |
|     |  - Layout Synthesis     |                                      |
|     |  - Markdown Formatting  |                                      |
|     +------------+------------+                                      |
|                  |                                                   |
|                  | State Transmit: {"report": "..."}                 |
|                  v                                                   |
|     +-------------------------+                                      |
|     |       END STATE         |                                      |
|     +-------------------------+                                      |
|                                                                      |
|  LLM Core Cognition Brain: [Groq Cloud APIs (Llama-3.3-70b-versatile)] |
+----------------------------------------------------------------------+

```
###Core Data State Flow

```
[START]
   │
   ▼
┌────────────────────────────────────────┐
│ State Initialized                      │
│ - topic: "User Input Query String"     │
│ - research_notes: ""                   │
│ - report: ""                           │
└──────────────────┬─────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────┐
│ researcher_node Execution              │
│ 1. Invokes DuckDuckGoSearchRun         │
│ 2. Sends Raw Results to Llama 3.3      │
│ 3. Updates State Schema                │
│    └─► research_notes = "Extracted..." │
└──────────────────┬─────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────┐
│ reporter_node Execution                │
│ 1. Reads research_notes from State     │
│ 2. Formulates Narrative Structure      │
│ 3. Updates State Schema                │
│    └─► report = "# Executive Summary..."│
└──────────────────┬─────────────────────┘
                   │
                   ▼
[END] ───► JSON Payload Returned to React View Layer

```
-----
#### live demo {[https://lanreact.vercel.app/]}
-----

# Autonomous Multi-Agent Research & Reporting Engine

An enterprise-grade, full-stack monorepo hosting an AI research workflow application. Built with **LangGraph** to coordinate multi-agent states, **Groq Cloud Infrastructure** powering lightning-fast reasoning, **FastAPI** for an asynchronous backend router, and **React JS** for an interactive analytics dashboard.

---

## 🚀 Key Features

- **State Graph Orchestration:** Uses [LangGraph](https://langchain.com) to build independent agent nodes that consume and update a shared, structured state schema.
- **Llama-3.3-70B Cognition Engine:** Deep contextual analytics and report generation powered by [Groq Cloud's](https://groq.com) ultra-low-latency interface.
- **Asynchronous Data Pipeline:** Built with [FastAPI](https://tiangolo.com) for structural input validation and rapid serverless execution.
- **Unified Monorepo Architecture:** Seamlessly configured for localized compilation or instant cloud hosting on [Vercel](https://vercel.com) using native micro-routing configurations.

---

## 📦 Project Directory Layout

```text
research-agent-app/
├── backend/
│   ├── main.py              # FastAPI Application & LangGraph Definition
│   └── requirements.txt     # Python Virtual Environment Dependencies
├── frontend/
│   ├── src/                 # React State UI Source Components
│   ├── index.html           # Document DOM Target Entry
│   ├── package.json         # Client Engine Build Config Matrix
│   └── vite.config.js       # Vite Engine Optimization Logic
└── vercel.json              # Monorepo Serverless Micro-Routing Manifest
```

---

## 🛠️ Local Development & Setup

### Prerequisites
- Python 3.10+ installed
- Node.js 18+ installed
- A valid **Groq Cloud API Key**

### 1. Backend Engine Configuration
Navigate to the backend directory, initialize your environment, and spin up the asynchronous runtime:

```bash
cd backend

# Initialize your virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install required components
pip install -r requirements.txt

# Create environment configuration file
echo "GROQ_API_KEY=your_actual_groq_api_key_here" > .env

# Run local runtime host
python main.py
```
The back-end server will spin up instantly at `http://localhost:8000`.

### 2. Frontend Layout Compilation
Open a separate terminal window and launch the user interface web engine:

```bash
cd frontend

# Install package dependencies
npm install

# Start local server instance
npm run dev
```
Open your browser to the designated URL (typically `http://localhost:5173`) to test the application.

---

## ☁️ Continuous Cloud Deployment with Vercel

This repository comes pre-packaged with a root-level `vercel.json` architecture map. To deploy the entire codebase to production seamlessly:

1. Install the global deployment tool asset:
   ```bash
   npm install -g vercel
   ```
2. Run the deployment setup from your root project directory:
   ```bash
   vercel
   ```
   *Note: When asked **"In which directory is your code located?"**, simply press **Enter** to default to your root folder path `./`.*
3. Navigate to your **Vercel Project Dashboard -> Settings -> Environment Variables** and securely add your secret parameter:
   - **Key:** `GROQ_API_KEY`
   - **Value:** `your_actual_groq_api_key`
4. Deploy your adjustments live to production:
   ```bash
   vercel --prod
   ```

---

## 🛡️ License
Distributed under the MIT License. See `LICENSE` inside the root tree directory for supplementary compliance information.
