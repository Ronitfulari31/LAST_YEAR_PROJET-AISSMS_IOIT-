# 🌐 InsightPoint AI News Intelligence Platform
### *B.Tech Final-Year Capstone Project Submission*
---

**InsightPoint AI** is a production-grade, state-of-the-art hybrid NLP intelligence pipeline designed to aggregate, translate, classify, extract metadata, and perform real-time multilingual sentiment analysis on unstructured news feeds and document streams. 

Equipped with a modern **Glassmorphic React Dashboard**, geospatial maps, sentiment volume distribution charts, and a high-throughput **Directed Acyclic Graph (DAG) Pipeline**, the platform resolves indication language barriers in disaster intelligence and news reporting.

---

## 📂 Submission Directory Layout
To ensure absolute clarity for the examination committee, the project is consolidated into two distinct sub-folders:

```text
LAST_YEAR_PROJECT/
├── 1_Project_Code/               # Raw Source Code & Assets
│   ├── Frontend/                 # React 19 / Vite / Tailwind UI Dashboard
│   ├── Backend/                  # Flask 3.1.0 RESTful API & Deep Learning Pipeline
│   ├── Database/                 # Seeding scripts, JSON samples, Schema Design
│   ├── package.json              # Global dependency configurations
│   └── requirements.txt          # Python dependency manifests
│
├── 2_Executable_File/             # Production Desktop Release
│   ├── InsightPoint_Launcher.exe  # Single-Click Compiled Desktop Service Launcher
│   ├── launcher.py               # Launcher script source code
│   └── Run_Instructions.txt      # Execution guide for examiners
│
├── package_project.py            # Automatic Packaging Script
└── README.md                     # Central Documentation (This File)
```

---

## ⚡ Single-Click Desktop Launcher
For convenience during evaluation, both the Backend Flask server and Frontend Vite React server can be booted simultaneously using our compiled **`InsightPoint_Launcher.exe`** executable!

### What it does:
1. **Prerequisite Check**: Validates if Python 3, Node.js, and MongoDB are installed on the examiner's machine.
2. **Auto Virtual Environment**: Automatically spins up a secure local Python virtual environment (`venv`) inside the packaged Backend directory.
3. **Silent Installer**: Automatically installs all deep learning and web framework pip requirements.
4. **Node package Manager**: Detects if Vite packages are missing and silently executes `npm install`.
5. **Parallel Daemon Processes**: Spawns both servers running concurrently in separate background threads.
6. **Automatic Browser Launch**: Instantly opens the default web browser to the dashboard URL: `http://localhost:5173`.

> **Note**: First-time boot can take 2-4 minutes while pip compiles the heavy machine learning binaries (PyTorch, transformers, SpaCy). Subsequent launches will boot **instantly** (less than 2 seconds)!

---

## 🛠️ System Technology Stack

### 💻 Frontend (Dashboard UI)
* **Framework**: React 19 (Component-driven UI architecture)
* **Build Engine**: Vite (Sub-second hot-reloads)
* **Styling**: Vanilla CSS + Glassmorphism design tokens (Premium, high-end aesthetics)
* **Data Visualization**: Recharts (Dynamic sentiment distributions & volumetric metrics)
* **Micro-Animations**: Custom CSS Keyframes and transition states (Responsive tactile feel)

### ⚙️ Backend (AI Core & REST API)
* **Server Framework**: Flask 3.1.0 (RESTful Python API endpoints)
* **Execution Architecture**: Custom Directed Acyclic Graph (DAG) Pipeline Orchestrator
* **AI Core Models**:
  * **Named Entity Recognition (NER)**: `GLiNER-large` (Zero-shot extraction of indicates locations and locations mapping)
  * **Neural Translation**: `facebook/nllb-200-1.3B` (Distilled No Language Left Behind, supports 9+ Indic languages)
  * **Category Classification**: `BART-large-MNLI` (Zero-shot category extraction)
  * **Multilingual Sentiment**: `RoBERTa-large` (Fine-tuned on high-volume news datasets)
  * **Vector Embeddings**: `intfloat/multilingual-e5-large` (For cross-lingual semantic search)
* **Database**: MongoDB (Flexible, high-throughput document store)

---

## 🗄️ Database Schema & Seeding
All schemas are designed to ensure high-performance indexing, unique constraint checks (preventing RSS scraper overlaps), and full relational traces.

### Collection Overview:
1. **`users`**: Manages session validation, email unique indexes, and user UI configurations (e.g. theme preference).
2. **`news_dataset`**: Manages news articles, NLP categories, geospatial mapping coordinates, and 1024-dimensional semantic search vectors.
3. **`documents`**: Manages user-uploaded documents (PDFs, DOCX, TXT) and pastes with full pipeline metric latency traces.

### 🚀 Instant Seed Configuration:
To populate the database with enriched pre-calculated machine learning records (enabling geospatial maps and charts to work out of the box), execute the seed script:
```bash
# Navigate to the database folder
cd 1_Project_Code/Database

# Run the seeding script
python seed_db.py
```

---

## 🔑 Manual Developer CLI Setup
If you wish to run the individual components manually via terminal CLI instead of using the single-click launcher:

### 1. Database Seeding
Ensure your local MongoDB instance is running, or verify your Cloud Atlas URI is configured inside `1_Project_Code/Backend/.env`.
```bash
cd Database
pip install pymongo python-dotenv
python seed_db.py
```

### 2. Run Backend Flask API
```bash
cd Backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

### 3. Run Frontend Vite React
```bash
cd Frontend
npm install
npm run dev
```
Open **`http://localhost:5173`** in your browser!

---
*© 2026 InsightPoint AI. B.Tech Engineering Capstone Project. All rights reserved.*
