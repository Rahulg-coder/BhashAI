# BhashAI — System Architecture Document
**Smart India Hackathon 2026 · Problem Statement SIH26042**

## 1. High-Level Vision
BhashAI is an offline-first vernacular pedagogy and real-time voice translation assistant designed specifically for primary schools in tribal regions of Jharkhand (starting with **Hindi → Santhali** using Ol Chiki script, architected to expand to **Mundari** and **Ho**).

---

## 2. Pipelined Architecture

```text
Teacher Speaks (Hindi)
        │
        ▼
Speech-to-Text (Whisper ASR)
        │
        ▼ Hindi Transcript
FLN Educational Context Engine
 (Grade, Subject, Domain, Outcome, Sentence Type)
        │
        ▼ Enriched Context & Glossary
Context-Aware Translation Engine (Santhali Ol Chiki / Mundari / Ho)
        │
        ▼ Candidate Translation
Translation Quality & Terminology Validator
 (Semantic, Terminology consistency, Confidence scoring)
        │
        ▼ Validated Text (Ol Chiki + Phonetic)
Text-to-Speech Engine (Santhali Audio)
        │
        ▼
Student Audio (.wav / .mp3) & On-Screen Visual Presentation
```

---

## 3. Real-Time Latency Budget (SIH $\le$ 3.0s Target)
- **Hindi ASR**: $\approx 400 - 800\text{ ms}$ (CUDA accelerated Whisper).
- **Context-Aware Translation & Validation**: $\approx 100 - 200\text{ ms}$.
- **Vernacular TTS Audio Generation**: $\approx 400 - 900\text{ ms}$.
- **Total Pipeline Latency**: $\approx 1.2 - 2.2\text{ seconds}$ (well within SIH $\le 3000\text{ ms}$ limit).

---

## 4. Offline-First Synchronization Architecture
```text
Android Tablet (Room + SQLite)
   │
   ├─ Offline Mode: Queries local SQLite Room DB for FLN outcomes, lessons, worksheets, flashcards, audio cache
   │
   └─ Online Mode (Incremental Sync):
         GET /api/v1/sync?version=12
         FastAPI server checks delta against MongoDB/Master JSON
         Returns new lessons, updated terminology, newly approved translations
         Android commits delta to SQLite and updates local version to 15
```

---

## 5. Security & Modular Language Providers
- No hardcoded secrets: `.env` and `.env.example` configurations.
- Abstract `LanguageProvider` with modular classes:
  - `SanthaliProvider` (`sat_Olck`)
  - `MundariProvider` (`mun`)
  - `HoProvider` (`ho`)
- Terminology Glossary enforces consistency across curriculum domains.
- Native Speaker Review database allows community validation and continuous dataset enrichment.
