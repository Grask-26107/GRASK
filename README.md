# GRASK AI

**Team Name: GRASK**  
**Smart India Hackathon 2026 | Problem Statement ID: SIH26107**  
*AI-Powered Intelligent Assistant for Indian Standards (BIS) & FSSAI Services for Industries and Consumers*

---

## 🌟 What is GRASK AI?

Navigating Indian industrial and food standards has traditionally required searching through fragmented portals, complex PDFs, and confusing statutory orders.

**GRASK AI** bridges this gap. It allows small business owners (MSMEs), laboratory testing engineers, and everyday citizens to ask questions in plain language (via text or voice across **11 Indian languages**), verify statutory licenses, navigate conformity schemes, assess certification readiness, and receive instant, 100% verified compliance answers backed by official statutory clauses.

---

## 🚀 Key Modules & Capabilities

### 1. 🛡️ Domain Relevance & Semantic Sanitizer Guard
- **Scope Validation**: Inspects inputs across all features. Automatically identifies and rejects out-of-scope topics with zero dummy data injection or state leakage.
- **Cross-Domain Separation**: Prevents domain contamination (e.g., food safety queries are separated from structural engineering standards).
- **Spelling & Grammar Repair**: Automatically corrects typos, phonetically romanized Indian terms, broken grammar, and technical entity names in the user's original language.

### 2. 🧭 BIS Scheme Finder / Certification Route Navigator (`SchemeFinderModal.tsx`)
- **Interactive 3-Step Decision Tree**: Guides manufacturers, importers, and MSMEs to their exact statutory compliance route.
- **Intelligent Scheme Matching**:
  * **Domestic Manufacturers**: Scheme-I (ISI Mark) for standard industrial goods.
  * **IT & Electronics**: Scheme-II (Compulsory Registration Scheme - CRS / MeitY).
  * **Foreign Manufacturers**: FMCS (Foreign Manufacturers Certification Scheme).
  * **Precious Metals**: Hallmarking Scheme for Gold & Silver (HUID).
  * **Eco Products**: Eco-Mark Certification.
- **Turnkey Guidance**: Provides official government portal links, statutory timelines, testing criteria, and MSME fee concessions with 1-click transition to Readiness Assessment.

### 3. 📋 Ready to Apply: MSME Readiness & Statutory Dossier Generator (`ReadyToApplyModal.tsx`)
- **Comprehensive Readiness Evaluation**: Assesses factory preparedness for BIS licensing across high-demand products (e.g., Drinking Water IS 14543/10500, TMT Steel IS 1786, Cement IS 269, Helmets IS 4151, Cables, etc.).
- **In-House Laboratory Equipment Checklist**: Details mandatory testing equipment (e.g., Universal Testing Machine, Chemical Benches, Autoclaves, Incubators) required on factory premises prior to inspection.
- **Statutory Document & Fee Calculator**: Checks required documentation (manufacturing unit ownership, electricity load, machinery list) and computes exact government fees with Udyam MSME discounts (50% concession for Micro/Small enterprises).
- **Digital Sealed Dossier PDF**: Generates and downloads a complete, audit-ready **Application Readiness Dossier PDF** with embedded QR code verification.

### 4. 🧪 Audit Compliance Studio (`ComplianceWorkspace.tsx`)
- **Automated Lab Audits**: Ingests test certificates and lab parameters via document upload or direct input.
- **Instant Statutory Verification**: Compares observed parameters (e.g., Lead in Drinking Water under IS 14543, Yield Strength in TMT Steel under IS 1786, Soundness in Cement under IS 269) against official BIS tolerance limits.
- **Sealed PDF Reports**: Generates formal, downloadable compliance audit certificates with digital verification QR codes in seconds.
- **Anti-Hallucination Fallback**: If parameters are ambiguous or incomplete, the audit is cleanly flagged without fabricated benchmarks.

### 5. 🥗 FSSAI Nutri-Score & Hidden Ingredient Auditor (`NutriScoreModal.tsx`)
- **Nutritional Parameter Analysis**: Evaluates nutritional breakdowns (energy, protein, carbohydrates, total sugar, added sugar, fats, sodium) and ingredients lists.
- **FSSAI Grading Engine**: Assigns a Front-of-Pack Nutri-Score Grade (A to E) and consumer-friendly safety verdict (`SECURE`, `CAUTION`, `HARMFUL`).
- **Hidden Additives Radar**: Detects hidden sugars (maltodextrin, invert syrup, HFCS), palm oil, and harmful industrial emulsifiers/preservatives.
- **Persona Warnings**: Contextual safety alerts for diabetic, hypertension, pediatric, and health-conscious consumer personas.

### 6. 🏷️ MANAK-Vision Statutory Mark Verifier (`LicenseVerifyModal.tsx`)
- **Comprehensive Identifier Support**:
  * **BIS ISI Mark**: 7 to 10-digit Scheme-I CM/L license codes.
  * **FSSAI License**: 14-digit central/state food safety licenses.
  * **Gold Hallmark**: 6-character alphanumeric Hallmarking Unique Identification (HUID) codes.
  * **MeitY CRS**: 8-digit Compulsory Registration Scheme (R-XXXXXXXX) numbers.
  * **GS1 Barcodes**: 13-digit EAN-13 barcodes (starting with `890` for India).
- **Counterfeit Detection**: Flags fake standard marks (e.g., ISI mark used without a valid statutory CM/L number).

### 7. 💬 Multilingual Standards AI Assistant (`ChatInterface.tsx`)
- **11 Indian Languages**: Real-time bilingual translation, speech-to-text (STT), and text-to-speech (TTS) in Hindi, Telugu, Tamil, Marathi, Bengali, Kannada, Gujarati, Malayalam, Punjabi, Urdu, and English.
- **Dual Personas**: Switch between **Citizen Mode** (plain language advice and consumer helpline guidance) and **Industry Mode** (exact clauses, penalties, and test methods).

### 8. 📊 Compliance Telemetry Dashboard (`TelemetryDashboard.tsx`)
- **Real-time Metrics**: Tracks query volume, response latency (<1s), compliance scores, and citizen feedback trends.

---

## 🔄 System Architecture

```
[ User Input: Statutory Query, Parameters, Voice, or Text ]
                          │
                          ▼
       [ 1. Domain Relevance & Semantic Sanitizer Guard ]
         ├─ Statutory Subject & Out-of-Scope Negative Pattern Classifier
         ├─ Cross-Domain Separation (Food vs Industrial vs Electronics)
         └─ Phonetic & Technical Entity Error Correction
                          │
         ┌────────────────┴────────────────┐
         ▼                                 ▼
   [ RELEVANT INPUT ]            [ IRRELEVANT INPUT ]
         │                                 │
         │                        • Immediate State Purge
         │                        • Alert Banner Displayed
         │                        • Zero Dummy Data Injection
         │
         ▼
   [ 2. Target Feature Processing ]
     ├─ Scheme Finder: 3-Step Conformity Route Decision Navigator
     ├─ Ready to Apply: Lab Machinery, Document & MSME Fee Dossier
     ├─ Audit Compliance: IS Benchmark Parameter Verification
     ├─ Nutri-Score: FSSAI Thresholds & Hidden Additive Audit
     ├─ MANAK-Vision: CM/L, FSSAI, CRS, HUID & Barcode Decoder
     └─ Standards Chat: ChromaDB Hybrid Vector + BM25 RAG
                          │
                          ▼
   [ 3. High-Speed Output & Verified Deliverables ]
     • Application Readiness Dossier PDFs with QR Verification
     • Digitally Sealed Audit PDF Certificates
     • Conformity Scheme Recommendations & Portal Handoffs
     • Nutri-Score FOPL Grades (A–E) & Health Alerts
     • Genuine vs Counterfeit Statutory Mark Verdicts
     • 11-Language Multilingual Spoken Responses
```

---

## ⚡ Quick Start Guide

### Prerequisites
- **Python**: Version 3.10 to 3.13
- **Node.js**: Version 18+ (Node 20+ recommended)
- **Google Gemini API Key**: Free key from [Google AI Studio](https://aistudio.google.com/)

---

### Step 1: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create environment file from template
# On Windows:
copy .env.example .env
# On Linux/macOS:
cp .env.example .env
```

Open `backend/.env` in any text editor and add your Gemini API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

Start the backend server:
```bash
python run.py
```
*Backend runs on `http://127.0.0.1:8000` (API documentation available at `http://127.0.0.1:8000/docs`).*

---

### Step 2: Frontend Setup

```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start Vite development server
npm run dev
```
*Frontend opens on `http://localhost:5173/`.*

---

## 🧪 Automated Testing & Evaluation Suite

GRASK includes an automated 800-query benchmark evaluation suite:

```bash
# Run the 800-query comprehensive SIH benchmark suite
python tests/test_800_comprehensive_sih_suite.py
```

### Benchmark Evaluation Highlights
- **Comprehensive 800-Query SIH Suite**: Validates RAG retrieval and clause accuracy across major Indian Standards (BIS) and FSSAI statutory regulations.

---

## 🔒 Security, Privacy & Safeguard Policies

- **Zero Credentials Exposure**: No live API keys, tokens, or personal identifiers are stored in the codebase or git repositories. All keys are read securely from local `.env` files.
- **Dynamic Relative Paths**: All storage paths, model caches, and database directories use portable relative paths (`./data`), ensuring compatibility across Windows, Linux, and macOS.
- **Rate-Limit Resilience**: Incorporates an intelligent cooldown guard for free-tier Gemini API quotas (429 errors), ensuring graceful fallbacks without user interruption.
- **Fail-Closed Verification**: Prevents hallucinated or guessed standards answers when statutory data is missing.

---

## 📜 License & Compliance

Developed for the **Smart India Hackathon 2026 (SIH26107)**.  
Built in compliance with statutory specifications published by the **Bureau of Indian Standards (BIS)** and the **Food Safety and Standards Authority of India (FSSAI)**.
