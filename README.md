# GRASK AI (v4.0)

**Team Name: GRASK**  
**Smart India Hackathon 2026 | Problem Statement ID: SIH26107**  
*AI-Powered Intelligent Assistant for Indian Standards (BIS) & FSSAI Services for Industries and Consumers*

---

## 🌟 What is GRASK AI?

Navigating Indian industrial and food standards has traditionally required searching through fragmented portals, complex PDFs, and confusing statutory orders.

**GRASK AI** bridges this gap. It allows small business owners (MSMEs), laboratory testing engineers, and everyday citizens to ask questions in plain language (via text or voice across **11 Indian languages**), capture physical product labels and lab reports via optical scanner, and receive instant, 100% verified compliance answers backed by official statutory clauses.

---

## 🚀 Key Modules & Capabilities

### 1. 🛡️ Domain Relevance & Semantic Sanitizer Guard
- **Vision Relevance Validation**: Inspects camera captures and file uploads across all features. Automatically identifies and rejects out-of-scope media (e.g., automobiles, vehicles, pets, landscapes, selfies, random noise) with zero dummy data injection or state leakage.
- **Cross-Domain Separation**: Prevents domain contamination (e.g., food nutrition labels are rejected in metal lab audits; structural steel reports are rejected in food safety).
- **Spelling & Grammar Repair**: Automatically corrects typos, phonetically romanized Indian terms, broken grammar, and technical entity names in the user's original language.

### 2. 🧪 Audit Compliance Studio (`ComplianceWorkspace.tsx`)
- **Automated Lab Audits**: Ingests test certificates and lab parameters via camera capture, scanned image, or PDF.
- **Instant Statutory Verification**: Compares observed parameters (e.g., Lead in Drinking Water under IS 14543, Yield Strength in TMT Steel under IS 1786, Soundness in Cement under IS 269) against official BIS tolerance limits.
- **Sealed PDF Reports**: Generates formal, downloadable compliance audit certificates with digital verification QR codes in seconds.
- **Anti-Hallucination Fallback**: If an image is irrelevant or parameters are unreadable, the audit is cleanly aborted without fabricated benchmarks.

### 3. 🥗 FSSAI Nutri-Score & Hidden Ingredient Auditor (`NutriScoreModal.tsx`)
- **OCR Label Scanning**: Extracts nutritional tables (energy, protein, carbohydrates, total sugar, added sugar, fats, sodium) and ingredients lists from food packages.
- **FSSAI Grading Engine**: Assigns a Front-of-Pack Nutri-Score Grade (A to E) and consumer-friendly safety verdict (`SECURE`, `CAUTION`, `HARMFUL`).
- **Hidden Additives Radar**: Detects hidden sugars (maltodextrin, invert syrup, HFCS), palm oil, and harmful industrial emulsifiers/preservatives.
- **Persona Warnings**: Contextual safety alerts for diabetic, hypertension, pediatric, and health-conscious consumer personas.

### 4. 🏷️ MANAK-Vision Statutory Mark Verifier (`LicenseVerifyModal.tsx`)
- **Multi-Symbology Optical Engine**: Reads 1D/2D optical barcode stripes (GS1 EAN-13 starting with `890`) and extracts printed statutory codes using hybrid optical recognition.
- **Comprehensive Identifier Support**:
  * **BIS ISI Mark**: 7 to 10-digit Scheme-I CM/L license codes.
  * **FSSAI License**: 14-digit central/state food safety licenses.
  * **Gold Hallmark**: 6-character alphanumeric Hallmarking Unique Identification (HUID) codes.
  * **MeitY CRS**: 8-digit Compulsory Registration Scheme (R-XXXXXXXX) numbers.
- **Counterfeit Detection**: Flags fake standard marks (e.g., ISI mark printed without a statutory CM/L number).

### 5. 💬 Multilingual Standards AI Assistant (`ChatInterface.tsx`)
- **11 Indian Languages**: Real-time bilingual translation, speech-to-text (STT), and text-to-speech (TTS) in Hindi, Telugu, Tamil, Marathi, Bengali, Kannada, Gujarati, Malayalam, Punjabi, Urdu, and English.
- **Dual Personas**: Switch between **Citizen Mode** (plain language advice and consumer helpline guidance) and **Industry Mode** (exact clauses, penalties, and test methods).

### 6. 📊 Compliance Telemetry Dashboard (`TelemetryDashboard.tsx`)
- **Real-time Metrics**: Tracks query volume, response latency (<1s), compliance scores, and citizen feedback trends.

---

## 🔄 System Architecture

```
[ User Input: Camera Capture, Image Upload, Voice, or Text ]
                          │
                          ▼
       [ 1. Domain Relevance & Semantic Sanitizer Guard ]
         ├─ Multimodal Vision & OCR Subject Classifier
         ├─ Out-of-Scope Negative Pattern Filtering
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
     ├─ Audit Compliance: IS Benchmark Parameter Verification
     ├─ Nutri-Score: FSSAI Thresholds & Hidden Additive Audit
     ├─ MANAK-Vision: CM/L, FSSAI, CRS, HUID & Barcode Decoder
     └─ Standards Chat: ChromaDB Hybrid Vector + BM25 RAG
                          │
                          ▼
   [ 3. High-Speed Output & Verified Deliverables ]
     • Digitally Sealed Audit PDF Certificates
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

GRASK includes an automated 50-image multimodal test suite to evaluate camera and optical scanner capabilities:

```bash
# Run the 50-image automated evaluation suite
python backend/run_50_image_eval.py

# Run the core domain relevance & typo correction unit tests
python backend/test_relevance_and_correction_suite.py
```

### Evaluation Benchmark Results (77 Tests Across 50 Images)
- **Audit Lab Reports Accuracy**: 12/12 Conforming/Non-Conforming reports verified.
- **FSSAI Nutri-Score Accuracy**: 13/13 Packaging labels graded with additive detection.
- **MANAK-Vision Accuracy**: 13/13 ISI, CRS, HUID, FSSAI, and GS1 codes identified.
- **Irrelevant Media Rejection Rate**: **100% rejection** across cars, machinery, pets, scenery, selfies, and noise.
- **Cross-Domain Separation**: **100% rejection** of mismatched domain media.
- **Overall Pass Rate**: **100.00% (77 / 77 Passed)**.

---

## 🔒 Security, Privacy & Safeguard Policies

- **Zero Credentials Exposure**: No live API keys, tokens, or personal identifiers are stored in the codebase or git repositories. All keys are read securely from local `.env` files.
- **Dynamic Relative Paths**: All storage paths, model caches, and database directories use portable relative paths (`./data`), ensuring compatibility across Windows, Linux, and macOS.
- **Rate-Limit Resilience**: Incorporates an intelligent cooldown guard for free-tier Gemini API quotas (429 errors), falling back instantly to local OCR (`tesseract.js`) without user interruption.
- **Fail-Closed Verification**: Prevents hallucinated or guessed standards answers when statutory data is missing.

---

## 📜 License & Compliance

Developed for the **Smart India Hackathon 2026 (SIH26107)**.  
Built in compliance with statutory specifications published by the **Bureau of Indian Standards (BIS)** and the **Food Safety and Standards Authority of India (FSSAI)**.
