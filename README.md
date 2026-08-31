# AI-Powered Vernacular Pedagogy & Real-Time Translation Tool

An AI-assisted translation and voice interaction system designed to support **Mother Tongue-Based Multilingual Education (MTB-MLE)** for primary school students in tribal regions.

The project aims to help Hindi-medium trained teachers deliver foundational literacy and numeracy content in tribal languages such as **Ho, Mundari, and Santhali**.

## 🎯 Problem

Many teachers working in tribal-area primary schools are trained primarily in Hindi and may not be proficient in the local tribal languages spoken by their students.

This creates a language barrier between teachers and students and makes it difficult to implement Mother Tongue-Based Multilingual Education effectively.

The proposed solution provides an AI-powered bridge between Hindi-speaking teachers and tribal-language-speaking students.

## 🚀 Current Prototype

For the initial prototype, we are focusing on:

**Hindi Speech → Hindi Text → Tribal Language Translation → Tribal Language Speech**

### Current Demo Flow

1. Teacher speaks a sentence in Hindi.
2. The system converts the Hindi speech into text.
3. The Hindi text is translated into the selected tribal language.
4. The translated text is displayed.
5. The translated text is converted into speech.
6. The generated audio can be played for the students.

## 🏗️ System Architecture

```text
Teacher
   │
   │ Hindi Speech
   ▼
Speech-to-Text
   │
   │ Hindi Text
   ▼
Translation Engine
   │
   │ Tribal Language Text
   ├───────────────► Display
   │
   ▼
Text-to-Speech
   │
   ▼
Tribal Language Audio
   │
   ▼
Student
```

## 📁 Project Structure

```text
vernacular-pedagogy-ai/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── services/
│       ├── speech_to_text.py
│       ├── translator.py
│       └── text_to_speech.py
│
├── frontend/
│
├── docs/
│   ├── problem-statement.md
│   ├── architecture.md
│   └── demo-progress.md
│
├── models/
├── data/
├── tests/
└── README.md
```

## 🧠 AI/NLP Components

The complete system is planned to contain:

* Hindi Speech Recognition
* Hindi → Tribal Language Translation
* Tribal Language Text-to-Speech
* Real-time Voice-to-Voice Translation
* Curriculum-aware translation
* Bilingual worksheet generation
* Visual flashcard generation
* Offline AI inference

## 📌 Prototype Scope

### Phase 1 — Voice Translation Demo

**Status: In Progress**

* [x] Project repository created
* [ ] Hindi speech input
* [ ] Hindi speech-to-text
* [ ] Hindi → tribal language translation
* [ ] Tribal language text output
* [ ] Tribal language text-to-speech
* [ ] End-to-end demo

### Phase 2 — Educational Content

* [ ] FLN lesson translation
* [ ] Activity instruction translation
* [ ] Assessment prompt translation
* [ ] Bilingual worksheet generation
* [ ] Flashcard generation

### Phase 3 — Real-Time Classroom Interaction

* [ ] Continuous speech recognition
* [ ] Voice-to-voice translation
* [ ] Response latency optimization
* [ ] Conversation handling

### Phase 4 — Offline Deployment

* [ ] Offline speech recognition
* [ ] Offline translation model
* [ ] Offline text-to-speech
* [ ] Android application
* [ ] Low-memory optimization
* [ ] Initial content synchronization

## 🎯 Long-Term Goal

The final application should operate on a low-cost Android tablet with approximately **2 GB RAM and Android 9+**, with core functionality available offline after initial content synchronization.

The target system should support:

**Hindi-speaking teacher ↔ Tribal-language-speaking student**

with minimal latency and educationally appropriate translations.

## 🛠️ Planned Technology Stack

| Component          | Technology                     |
| ------------------ | ------------------------------ |
| Backend            | Python                         |
| API                | FastAPI                        |
| Speech Recognition | Whisper / lightweight ASR      |
| Translation        | NLP Translation Model          |
| Text-to-Speech     | TTS Engine                     |
| Frontend           | To be implemented              |
| Mobile             | Android                        |
| Offline Inference  | Lightweight / quantized models |

## 📊 Current Development Strategy

We are following an incremental approach:

```text
Basic Translation
       ↓
Voice Input
       ↓
Voice Output
       ↓
Real-Time Interaction
       ↓
Educational Content Generation
       ↓
Offline Android Deployment
```

Rather than attempting the complete system at once, the prototype first validates the core Hindi-to-tribal-language voice translation pipeline.

## 👥 Team

Developed as part of the proposed solution for the AI-powered vernacular pedagogy and real-time translation challenge.

## 📜 License

This project is currently developed as a prototype for educational and hackathon evaluation purposes.
