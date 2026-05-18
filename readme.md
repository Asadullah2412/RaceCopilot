# 🏁 Race Copilot

[app link](https://racecopilot.streamlit.app/)

> A production-style AI race engineer assistant for sim racers, powered by the Google Gemini GenAI API.

Pit Wall AI is a domain-specialized conversational assistant built for sim racing drivers. Instead of acting like a generic chatbot, Pit Wall AI behaves like a virtual GT race engineer — analyzing driver debriefs, diagnosing handling problems, suggesting setup adjustments, and coaching driving technique.

The application is designed with real-world AI engineering principles in mind:

* modular architecture
* structured LLM outputs
* reusable prompt engineering
* production-ready API handling
* conversational memory
* scalable UI design

---

# 📸 Overview

Pit Wall AI allows drivers to:

* Submit race debriefs in natural language
* Receive structured engineering analysis
* Diagnose car balance and handling issues
* Get setup recommendations
* Learn track-specific driving techniques
* Continue contextual follow-up conversations

The system is optimized for racing simulators such as:

* Assetto Corsa Competizione
* iRacing
* F1 24
* rFactor 2
* Automobilista 2
* Gran Turismo 7

---

# ✨ Features

## 🧠 AI Race Engineer

The chatbot acts as a professional race engineer capable of:

* analyzing driver feedback
* identifying handling characteristics
* suggesting driving improvements
* recommending setup changes
* providing strategic race advice

---

## 📊 Structured AI Responses

Unlike traditional chatbots that return large unstructured paragraphs, Pit Wall AI generates structured JSON responses.

This enables:

* telemetry-style UI rendering
* engineering dashboards
* categorized diagnostics
* cleaner frontend architecture
* more predictable AI outputs

Example output sections:

* Corner Notes
* Car Diagnosis
* Setup Changes
* Driving Notes
* Track Insight
* Follow-Up Questions

---

## 💬 Conversational Follow-Up System

Drivers can continue discussing:

* specific corners
* setup adjustments
* tire behavior
* braking technique
* race strategy

The system maintains contextual conversation history for more natural interactions.

---

## 🎨 Motorsport-Inspired UI

The interface is inspired by:

* GT3 pit wall dashboards
* telemetry software
* endurance racing engineering tools
* professional motorsport timing systems

UI design highlights:

* dark engineering theme
* telemetry-inspired typography
* structured analysis cards
* compact information density
* racing-focused UX

![alt text](<ui.png>)

---

# 🏗️ System Architecture

The project follows a modular AI engineering architecture.

```text
User
  ↓
Streamlit UI
  ↓
Conversation / Session Manager
  ↓
Prompt Engineering Layer
  ↓
Gemini Service Layer
  ↓
Google Gemini API
```

---

# 📂 Project Structure

```text
project/
│
├── app.py                 # Streamlit frontend
├── gemini_client.py       # Gemini API service layer
├── prompts.py             # Prompt templates
├── requirements.txt
├── .env
│
├── utils/
│   ├── parser.py
│   ├── validators.py
│   └── logger.py
│
└── assets/
```

---

# ⚙️ Technologies Used

| Technology             | Purpose                     |
| ---------------------- | --------------------------- |
| Python                 | Core application logic      |
| Streamlit              | Interactive frontend UI     |
| Google Gemini API      | LLM reasoning engine        |
| JSON Structured Output | Reliable UI rendering       |
| Session State          | Conversational memory       |
| Custom CSS             | Motorsport-themed interface |

---

# 🧩 Prompt Engineering Strategy

Pit Wall AI uses modular prompt engineering instead of hardcoded prompts.

The system prompt defines the assistant as:

* a professional race engineer
* technically precise
* concise and actionable
* focused on realistic racing advice

The application uses specialized prompt flows for:

* driver debrief analysis
* setup coaching
* driving technique
* follow-up discussions
* strategy assistance

---

# 🔐 API Security & Environment Variables

API keys are securely managed using environment variables.

Example:

```env
GEMINI_API_KEY=your_api_key_here
```

The API layer is fully separated from the UI layer for cleaner architecture and easier scaling.

---

# 🛡️ Error Handling

The application includes:

* API exception handling
* fallback responses
* invalid JSON handling
* session management
* response validation
* graceful failure recovery

This ensures a more production-ready AI experience.

---

# 🚀 Running the Project

## 1. Clone the Repository

```bash
git clone <repository-url>
cd pitwall-ai
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## 5. Launch the Application

```bash
streamlit run app.py
```

---

# 📈 Example Workflow

## Driver Input

> “Rear feels unstable through Eau Rouge and I keep losing traction exiting Bus Stop.”

---

## AI Engineer Output

### Car Diagnosis

* Rear instability under compression
* Excessive throttle aggression on exit

### Setup Suggestions

* Increase rear wing slightly
* Reduce differential preload

### Driving Advice

* Smoother throttle application
* Reduce steering angle at apex exit

### Track Insight

* Focus on steering release timing through Eau Rouge compression

---

# 🧠 Production Engineering Concepts Demonstrated

This project demonstrates several real-world AI engineering concepts:

* modular AI architecture
* prompt engineering
* structured LLM outputs
* conversational memory
* token optimization
* API abstraction
* frontend/backend separation
* session state management
* domain-specialized copilots
* scalable UI rendering

---

# 🔮 Future Improvements

Potential future upgrades include:

* telemetry file upload support
* MoTeC integration
* AI race strategy planning
* voice engineer mode
* live session coaching
* vector database memory
* RAG-based racing knowledge system
* setup recommendation engine
* personalized driver profiles

---

# 🎯 Project Goal

The objective of Pit Wall AI is to demonstrate how modern LLM systems can evolve beyond generic chatbots into specialized AI copilots with:

* domain expertise
* structured reasoning
* scalable architecture
* production-oriented design

---

# 👨‍💻 Author

Built as an AI engineering project focused on:

* GenAI application development
* prompt engineering
* production-grade architecture
* conversational AI systems
* motorsport-focused user experience

---

# 🏁 Final Note

Pit Wall AI is not designed to replace real-world race engineers.

Instead, it explores how modern generative AI systems can assist sim racers by transforming natural language driver feedback into actionable technical insights.

The project represents a blend of:

* AI engineering
* motorsport knowledge
* software architecture
* user experience design
* conversational systems
