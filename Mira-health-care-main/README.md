# MIRA – Health Prediction Application
### Junior AI/ML Developer Task 1 | Gokul Infocare

A full-stack health prediction web application built with **FastAPI** (Python backend), **SQLite** (persistent storage), and **Bootstrap 5** (frontend). Uses the **Google Gemini AI API** to generate intelligent health remarks from patient blood test results.

---

## Features

- **CRUD Operations** – Create, Read, Update, and Delete patient records
- **AI-Powered Remarks** – Gemini AI analyses Glucose, Haemoglobin, and Cholesterol values and generates a clinical health assessment
- **Data Validation** – Frontend and backend validation (email format, future DOB check, positive numeric values)
- **Persistent Storage** – SQLite database via SQLAlchemy ORM
- **Clean UI** – Responsive Bootstrap 5 interface with colour-coded blood value indicators and live search

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+, FastAPI, Uvicorn |
| Database | SQLite + SQLAlchemy ORM |
| AI/ML API | Google Gemini 2.0 Flash |
| Frontend | HTML5, CSS3, Bootstrap 5, Vanilla JS |
| Validation | Pydantic v2 (backend), JS (frontend) |

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/mira-health-prediction.git
cd mira-health-prediction
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
```
Open `.env` and add your Gemini API key:
```
use gsk api key [I used this one ]

Instead of Gemini API, I'll switch the app to use Groq API — it's also completely free, gives AIza-style keys, and is actually faster. Here's how:
Step 1 — Go to https://console.groq.com
Step 2 — Sign up with Google (free, no credit card)
Step 3 — Click "API Keys" → "Create API Key"
Step 4 — Copy the key (starts with gsk_...)

OR 

GEMINI_API_KEY=your_actual_key_here
```
Get a free key at: https://aistudio.google.com/app/apikey

### 4. Run the application
```bash
uvicorn main:app --reload
```

### 5. Open in browser
```
http://localhost:8000
```

---

## Project Structure

```
mira_app/
├── main.py            # FastAPI app, routes, Gemini API integration
├── database.py        # SQLAlchemy engine and session
├── models.py          # Patient database model
├── schemas.py         # Pydantic request/response schemas with validation
├── requirements.txt   # Python dependencies
├── .env.example       # Environment variable template
├── .gitignore         # Excludes .env and DB files
└── static/
    └── index.html     # Full frontend (Bootstrap 5 + Vanilla JS)
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/patients/` | Get all patient records |
| POST | `/patients/` | Create new patient + AI remarks |
| GET | `/patients/{id}` | Get single patient |
| PUT | `/patients/{id}` | Update patient + regenerate AI remarks |
| DELETE | `/patients/{id}` | Delete patient record |

Interactive API docs available at: `http://localhost:8000/docs`

---

## Normal Reference Ranges

| Test | Normal Range |
|---|---|
| Glucose | 70–99 mg/dL (fasting) |
| Haemoglobin | 12–15.5 g/dL (women), 13.5–17.5 g/dL (men) |
| Cholesterol | Below 200 mg/dL |

---

*Built by Tejaswini H N | Trainee Software Engineer*
