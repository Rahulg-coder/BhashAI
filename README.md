# 🗣️ BhashAI — Vernacular Pedagogy & Real-Time Classroom Translation

[![Smart India Hackathon 2026](https://img.shields.io/badge/SIH-2026-blue.svg)](https://sih.gov.in)
[![Problem Statement](https://img.shields.io/badge/Problem%20Statement-SIH26042-orange.svg)](https://sih.gov.in)
[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.138%2B-green.svg)](https://fastapi.tiangolo.com)
[![Whisper ASR](https://img.shields.io/badge/ASR-Whisper%20CUDA-purple.svg)](https://github.com/openai/whisper)
[![Languages](https://img.shields.io/badge/Languages-Hindi%20%E2%86%92%20Santhali%20%7C%20Mundari%20%7C%20Ho-red.svg)](#supported-tribal-languages)

An offline-first AI teaching assistant designed for **Mother Tongue-Based Multilingual Education (MTB-MLE)** in tribal primary schools of Jharkhand. 

BhashAI allows Hindi-medium teachers to deliver foundational concepts by speaking Hindi, while the system instantaneously transcribes, enriches with educational context, validates terminology, and delivers **Santhali (Ol Chiki `sat_Olck`)** text and speech in **$\le 3$ seconds**, with a modular architecture ready for **Mundari** and **Ho**.

---

## 🎯 Key Features & SIH Differentiators

1. **Context-Aware Educational Translation**: Not a generic translator. Injects Grade (1-3), Subject (Math/Language), NIPUN Bharat FLN Domain, and Sentence Type to ensure pedagogically correct translations.
2. **Approved Educational Terminology Glossary**: Prevents mathematical and instructional terms (गिनती, जोड़, घटाव, शिक्षक, किताब) from fluctuating across lessons.
3. **Pipelined Real-Time Speech**: Hindi voice $\to$ Whisper ASR $\to$ Context Translation $\to$ Santhali TTS with latency tracking meeting the $\le 3000\text{ ms}$ requirement.
4. **Official NIPUN Bharat / FLN Content**: 1:1 mapped to official learning outcome codes (e.g. `FLN-M1-LO1`).
5. **Bilingual Student Worksheets**: Generates printable worksheets with dual-language instructions, visual hints, and answer keys.
6. **Visual Bilingual Flashcards**: Pedagogical cards with emojis/visuals, Hindi text, Ol Chiki script, phonetic guides, and native audio.
7. **Offline-First Room/SQLite Sync**: Works 100% offline after initial sync using incremental content versioning.
8. **Human-in-the-Loop Validation**: Enables native teachers and community reviewers to evaluate translations, submit corrections, and expand the persistent glossary.

---

## 🏗️ System Architecture

```text
Teacher Speaks (Hindi)
        │
        ▼
Speech Recognition (Whisper CUDA ASR)
        │
        ▼ Hindi Transcript
FLN Educational Context Engine
 (Grade 1-3 · Subject · FLN Domain · Learning Outcome · Sentence Type)
        │
        ▼ Context-Enriched Prompt
Vernacular Translation Provider (Santhali Ol Chiki sat_Olck / Mundari / Ho)
        │
        ▼ Candidate Translation
Translation Quality & Terminology Validator
 (Semantic consistency · Glossary match · Confidence score)
        │
        ▼ Approved Native Text & Phonetic Guide
Speech Synthesis Engine (Santhali Audio .wav / .mp3)
        │
        ▼
Student Audio Playback & Classroom Visual Display
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.12.7)
- `ffmpeg` installed on your system PATH
- NVIDIA GPU with CUDA recommended (CPU supported with automatic fallback)

### 2. Environment Setup
```powershell
# Clone and enter the repository
cd BhashAI/backend

# Create & activate virtual environment (optional if using global python)
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run Automated Integration Tests
```powershell
# Set UTF-8 encoding in PowerShell
$env:PYTHONIOENCODING="utf-8"

# Run the 10-module comprehensive test suite
python -m unittest tests/test_all_services.py
```
*Expected Output: `Ran 10 tests in ~7s ... OK`*

### 4. Start the FastAPI Backend Server
```powershell
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 5. Launch the Teacher Tablet UI
Open `frontend/index.html` directly in your browser:
```powershell
start ../frontend/index.html
```
Or open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive Swagger API documentation.

---

## 📁 Repository Structure

```text
BhashAI/
│
├── backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── health.py            # Health diagnostics & status
│   │   │   │   ├── routes_asr.py        # POST /api/v1/asr
│   │   │   │   ├── routes_translation.py# POST /api/v1/translate
│   │   │   │   ├── routes_tts.py        # POST /api/v1/tts & audio serving
│   │   │   │   ├── routes_live.py       # POST /api/v1/live-translate (<=3s)
│   │   │   │   ├── routes_fln.py        # GET /api/v1/fln/outcomes & lessons
│   │   │   │   ├── routes_worksheets.py # POST /api/v1/worksheets/generate
│   │   │   │   ├── routes_flashcards.py # POST /api/v1/flashcards/generate
│   │   │   │   ├── routes_validation.py # POST /api/v1/validation/review
│   │   │   │   └── routes_sync.py       # GET /api/v1/sync (incremental)
│   │   │   └── api.py                   # Central V1 router
│   │   ├── services/
│   │   │   ├── asr_service.py           # Whisper ASR with CUDA detection
│   │   │   ├── languages.py             # Santhali, Mundari, Ho providers
│   │   │   ├── glossary_service.py      # Educational terminology glossary
│   │   │   ├── translation_service.py   # Context-aware translation
│   │   │   ├── validation_service.py    # Translation confidence & checks
│   │   │   ├── tts_service.py           # Vernacular speech synthesis
│   │   │   ├── fln_service.py           # NIPUN Bharat curriculum & lessons
│   │   │   ├── worksheet_service.py     # Bilingual worksheet generator
│   │   │   ├── flashcard_service.py     # Visual flashcard generator
│   │   │   ├── sync_service.py          # Delta sync engine
│   │   │   └── validation_review_service.py # Native speaker review store
│   │   └── config.py                    # Settings & .env loader
│   ├── tests/
│   │   ├── test_health.py               # Health unit tests
│   │   └── test_all_services.py         # Full integration test suite
│   ├── main.py                          # FastAPI application bootstrap
│   └── requirements.txt                 # Backend dependencies
│
├── data/
│   ├── fln/
│   │   ├── curriculum.json              # Official NIPUN Bharat FLN data
│   │   └── lessons.json                 # Structured pedagogical lessons
│   ├── terminology/
│   │   └── glossary.json                # Approved multilingual glossary
│   ├── audio_cache/                     # Pre-cached audio files
│   └── validation_reviews.json          # Native speaker validation log
│
├── frontend/
│   └── index.html                       # Responsive Teacher Tablet UI
│
├── android/
│   └── README.md                        # Android Room + SQLite architecture
│
├── docs/
│   ├── architecture.md                  # Comprehensive system design
│   ├── problem-statement.md             # SIH26042 background & rationale
│   ├── evaluation.md                    # Latency & quality benchmarks
│   └── demo-progress.md                 # 14-phase implementation tracker
│
├── README.md
└── .gitignore
```

---

## 📡 API Endpoint Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Server status, version, and component readiness |
| `POST` | `/api/v1/asr` | Transcribe Hindi speech into Devanagari text |
| `POST` | `/api/v1/translate` | Context-aware translation to Santhali (Ol Chiki), Mundari, Ho |
| `POST` | `/api/v1/tts` | Synthesize native tribal speech audio |
| `GET` | `/api/v1/tts/audio/{file}` | Stream cached `.mp3` / `.wav` audio |
| `POST` | `/api/v1/live-translate` | End-to-end real-time pipeline with latency metrics |
| `GET` | `/api/v1/fln/outcomes` | Retrieve official NIPUN Bharat learning outcomes |
| `GET` | `/api/v1/fln/lessons` | Retrieve structured classroom lessons |
| `POST` | `/api/v1/worksheets/generate` | Generate FLN-aligned bilingual printable worksheets |
| `POST` | `/api/v1/flashcards/generate` | Generate visual bilingual flashcards with audio |
| `POST` | `/api/v1/validation/review` | Submit native speaker review / correction |
| `GET` | `/api/v1/sync` | Incremental delta synchronization for offline devices |

---

## 👥 Hackathon Team & Evaluation
Developed for **Smart India Hackathon 2026** (Problem Statement **SIH26042**).
- **Primary Focus**: Mother Tongue-Based Multilingual Education (MTB-MLE).
- **Target Region**: Jharkhand primary schools.
- **Languages**: Hindi $\to$ Santhali (Ol Chiki), expandable to Mundari & Ho.
