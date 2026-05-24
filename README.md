# Arcn

A modular AI assistant built from the ground up in Python. Not a wrapper around an API — every component is understood, designed, and built deliberately.

Arcn listens to what you say, understands what you mean, and does it. It runs entirely on your machine.

---

## What it does

- Understands natural language commands across 20 intent categories
- Remembers context across a conversation — follow-ups, references, corrections
- Executes real actions: opens apps, searches the web, controls system volume and brightness, sets timers, takes notes, tells the time and date
- Runs fully offline — no cloud, no subscriptions, no data leaving your machine

---

## Architecture

Arcn is built as a set of independent cognitive modules, each with a single responsibility, coordinated through a central orchestration layer.

```
Voice / Text
     │
     ▼
  NLP Module          ← understands language, extracts intent and entities
     │
     ▼
Command Center        ← orchestrates, routes, and decides what to do
     │
     ▼
 Tools Module         ← executes the actual actions
```

The defining principle: no module does another module's job. The NLP doesn't execute actions. The Command Center doesn't parse language. Clean contracts between everything.

---

## Modules

### NLP Module
The language understanding layer. Processes raw text into a structured packet the Command Center can act on.

- Fine-tuned DistilBERT trained on 300 examples across 20 intent categories
- Confidence scoring with automatic unknown intent detection
- spaCy NER + regex for entity extraction (durations, times, people, apps, locations)
- 10-turn context window with slot accumulation, follow-up detection, and vague reference resolution

Output:
```python
{
    "intent": "set_timer",
    "confidence": 0.921,
    "entities": {"duration": "10 mins"},
    "requires_clarification": False,
    "context_used": False
}
```

### Command Center
The orchestration core. Receives structured packets and decides what to do with them.

- Routes intents and entities to the right tool
- Handles unknown intents and clarification requests
- Manages system state
- Designed to support agentic and multi-step behaviors as the system grows

### Tools Module
The execution layer. A registry of real actions the system can take.

- App launching (YouTube, Chrome, Terminal, VS Code, Notes, Finder, Settings)
- System controls (volume, brightness, lock)
- Web search (Google, YouTube)
- Timer with Mac notification
- Notes saved to disk with timestamps
- Time and date
- Developer and study workspace modes

---

## Roadmap

- [x] NLP — intent classification, entity extraction, multi-turn context
- [x] Command Center — orchestration, routing, state management
- [x] Tools — real Mac actions across 20 intent categories
- [ ] Speech — voice input via Whisper, voice output via Edge TTS
- [ ] Memory — persistent context across sessions with vector retrieval
- [ ] Computer Vision — gesture recognition, screen analysis, object understanding via LLaVA
- [ ] Logs & Validator — action auditing, confidence checks, safety layer
- [ ] main.py — single entry point that boots the full system
- [ ] Ambient UI — visual state feedback

---

## Setup

**Requirements:** Python 3.12, macOS (Mac-first, cross-platform support planned)

```bash
git clone https://github.com/foxCoder-star/Arcn.git
cd Arcn
```

**NLP module:**
```bash
cd nlp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m spacy download en_core_web_sm
python3 train_intent.py
deactivate
```

**Command Center:**
```bash
cd ../command_center
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

**Tools:**
```bash
cd ../tools_assistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

**Run:**
```bash
cd command_center
source venv/bin/activate
python3 test_wired.py
```

---

## Tech Stack

- Python 3.12
- HuggingFace Transformers — DistilBERT fine-tuning
- PyTorch — model training and inference
- spaCy — named entity recognition
- faster-whisper — local speech recognition (coming)
- Edge TTS — neural voice output (coming)
- Ollama + Mistral 7B — local knowledge engine (coming)
- MediaPipe — gesture recognition (coming)
- LLaVA — vision and screen understanding (coming)

---

## Status

Core pipeline — NLP → Command Center → Tools — is fully operational. The system correctly understands natural language, routes to the right action, and executes it locally.

Everything from here builds on top of a working foundation.

---

Built by David Mishael.
