# GRASK

**Team Name: GRASK**  
**Smart India Hackathon 2026 | Problem Statement ID: SIH26107**  
*AI-Powered Intelligent Assistant for Indian Standards (BIS) & FSSAI Services for Industries and Consumers*

---

## 🌟 What is GRASK AI?

Navigating Indian industrial and food standards has traditionally required searching through fragmented portals, complex PDFs, and confusing statutory orders.

**GRASK AI** bridges this gap. It allows small business owners (MSMEs), testing engineers, and everyday citizens to ask questions in plain language (via text or voice in **11 Indian languages**) and receive instant, 100% verified answers backed by official statutory clauses.

---

## 🔄 User Input to Result: How It Works

```
[ User Input (Text or Voice) ]
  • Any of 11 Indian Languages (Hindi, Telugu, Tamil, English, etc.)
  • Informal speech, trade slang, or typos accepted
                │
                ▼
[ 1. Security & Intent Engine ]
  • Blocks prompt-injection attacks & redacts sensitive personal data
  • Identifies intent: Standard query, Lab test, License check, or Food safety
                │
                ▼
[ 2. Table-Aware Dual Retrieval ]
  • Exact Alphanumeric Match (e.g., IS 14543, IS 10500)
  • Hybrid Semantic Search (ChromaDB Vector + BM25 Keyword Search)
  • Preserves complex chemical limits and tolerance tables intact
                │
                ▼
[ 3. Fail-Closed Verification Engine ]
  • Cross-checks answers against official Bureau of Indian Standards clauses
  • Anti-Hallucination Guardrail: If confidence < 0.40 or standards conflict,
    it refuses to guess and escalates to National Consumer Helpline 1915
                │
                ▼
[ 4. Instant Output & Action Studio ]
  • Citizen Advice: Plain-language summary & consumer rights
  • Industry Mode: Exact statutory clauses, limits, and testing methods
  • 1-Click Sealed PDF Lab Audit Report / 11-Language Voice Readout
```

---

## 🚀 Key Features & Modules

Every feature in GRASK AI is designed to solve a specific, real-world regulatory challenge:

### 1. 💬 Multilingual Conversational Assistant (`ChatInterface.tsx`)
* **Natural Dialogue**: Accepts messy, ungrammatical, or technical queries.
* **11 Indian Languages**: Full speech-to-text (STT) and text-to-speech (TTS) in Hindi, Telugu, Tamil, Marathi, Bengali, Kannada, Gujarati, Malayalam, Punjabi, Urdu, and English.
* **Dual Personas**: Switch between **Citizen Mode** (simple explanations) and **Industry Mode** (exact clauses, penalties, and test methods).

### 2. 🏷️ License & Hallmark Scanner (`LicenseVerifyModal.tsx`)
* **Instant Verification**: Validates BIS CM/L license numbers, CRS registration numbers, and 6-digit Gold HUID hallmarks in under 1 second.
* **Counterfeit Protection**: Tells citizens immediately whether an ISI or Hallmark stamp on a product is genuine or fake.

### 3. 🥗 Nutri-Score & Food Safety Analyzer (`NutriScoreModal.tsx`)
* **OCR Label Scanning**: Upload photos of food labels to extract nutritional values (sugar, sodium, saturated fat).
* **FSSAI Grading**: Automatically assigns a Nutri-Grade (A to E) and flags hidden toxic additives or banned industrial dyes.

### 4. 🧪 Lab Audit & Compliance Studio (`ComplianceWorkspace.tsx`)
* **Automated Lab Audits**: Engineers can input or upload lab test results for any standard (e.g., Lead in Drinking Water, Yield Strength in TMT Steel).
* **Instant Verification**: Automatically evaluates every parameter against statutory limits with a Pass/Fail verdict.
* **Sealed PDF Reports**: Generates formal, downloadable audit certificates with digital verification QR codes in seconds.

### 5. 🏛️ BIS & FSSAI Services Directory (`BisServicesModal.tsx`)
* **Unified Knowledge Base**: Access details for 24,000+ Indian standards, mandatory Quality Control Orders (QCOs), testing laboratories, and application fee waivers (including 50% startup discounts).

### 6. 📊 Compliance Telemetry Dashboard (`TelemetryDashboard.tsx`)
* **Real-time Oversight**: Tracks query volume, response latency (<1s), compliance scores, and citizen feedback trends.

---

## 🔑 API Key Setup (Where to Add & Why)

### 📌 Where to Paste Your API Key
1. Navigate to the `backend/` folder:
   ```bash
   cd backend
   ```
2. Create a local `.env` file by copying `.env.example`:
   ```bash
   # On Windows:
   copy .env.example .env

   # On Linux/macOS:
   cp .env.example .env
   ```
3. Open `.env` in any text editor and paste your key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```
   *(You can generate a free Gemini API key at [Google AI Studio](https://aistudio.google.com/)).*

> [!NOTE]
> The `.env` file is listed in `.gitignore` so your personal API key will **never** be uploaded to GitHub.

### ❓ Why Is the API Key Needed?
GRASK AI uses **Google Gemini API** for:
1. **Natural Dialogue & Translation**: Understands regional trade slang, colloquial phrasing, and translates statutory legal English into 11 Indian languages.
2. **Contextual Reasoning**: Resolves ambiguous product descriptions (e.g., *"plastic pipe for farm borewell"*) to the exact statutory Indian Standard (`IS 4984`).
3. **Semantic Embeddings**: Generates mathematical vector embeddings (`text-embedding-004`) to search 24,000+ standards clauses with high accuracy.

*(Offline Fallback: If no API key is set, the system automatically falls back to deterministic local RAG keyword search without crashing).*

---

## 🧪 Validated 800-Query Benchmark Suite

GRASK AI's accuracy is backed by an automated 800-query benchmark dataset covering 8 core regulatory domains:

| Benchmark Domain | Queries | Pass Rate | Hallucination Rate |
| :--- | :---: | :---: | :---: |
| 1. Indian Standards Technical Q&A | 100 | 100% | 0.00% |
| 2. Product Description to IS Code Mapping | 100 | 99.0% | 0.00% |
| 3. BIS Certification Schemes (I, II, FMCS) | 100 | 100% | 0.00% |
| 4. Certification & Application Procedures | 100 | 100% | 0.00% |
| 5. Consumer Rights & Grievance (Helpline 1915) | 100 | 100% | 0.00% |
| 6. Gold & Silver Hallmarking (6-digit HUID) | 100 | 100% | 0.00% |
| 7. Testing Laboratories & NABL Methods | 100 | 99.0% | 0.00% |
| 8. Multilingual Script Integrity & Red-Teaming | 100 | 99.0% | 0.00% |
| **Overall System Performance** | **800** | **99.6%** | **0.00%** |

*All test queries and benchmark results are available under `tests/` (`test_queries_800_dataset.json` & `test_results_800.json`).*

---

## 📁 Repository Structure

```text
├── backend/
│   ├── app/
│   │   ├── api/             # REST endpoints (chat, audit, standards, telemetry)
│   │   ├── core/            # Config, database, security firewall
│   │   ├── models/          # Data schemas and validation
│   │   └── services/        # RAG engine, hybrid search, table parser, verifier
│   ├── data/
│   │   ├── chroma_db/       # Pre-indexed standards vector database
│   │   ├── uploads/         # Official sample standards PDFs
│   │   └── reports/         # Generated audit reports
│   ├── .env.example         # Environment template with safe defaults
│   ├── requirements.txt     # Python dependencies
│   └── run.py               # Backend startup entrypoint
├── frontend/
│   ├── src/
│   │   ├── components/      # UI components (Chat, Audits, Modals, Dashboard)
│   │   ├── services/        # API client bindings
│   │   └── App.tsx          # Main application component
│   ├── package.json         # Frontend dependencies (React + Tailwind + Vite)
│   └── vite.config.ts       # Vite proxy & build settings
├── tests/
│   ├── test_800_comprehensive_sih_suite.py  # 800-query validation runner
│   ├── test_queries_800_dataset.json        # 800 curated test cases
│   └── test_results_800.json                # Benchmark output logs
└── README.md
```

---

## ⚡ Quick Start Guide

### 1. Prerequisites
* Python 3.10+
* Node.js 18+

### 2. Backend Setup
```bash
cd backend
python -m venv venv

# Activate virtual environment:
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt

# Create .env and paste your GEMINI_API_KEY
copy .env.example .env    # On Linux/macOS: cp .env.example .env

python run.py
```
*Backend starts on `http://localhost:8000` (API docs at `http://localhost:8000/docs`).*

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
*Frontend opens at `http://localhost:5173`.*

### 4. Running the Benchmark Test Suite
```bash
python tests/test_800_comprehensive_sih_suite.py
```

---

*Developed for Smart India Hackathon 2026 | Bureau of Indian Standards & FSSAI Unified Intelligence.*
