# EduGenie

EduGenie is an AI-powered educational assistant built using FastAPI,
HTML, CSS, JavaScript, and Google Gemini.

## Features

- Ask academic questions
- Explain difficult concepts
- Generate 3-question MCQ quizzes
- Summarize educational text
- Generate personalized learning paths
- Optional local LaMini-Flan-T5 explanation model
- Responsive web interface
- REST API
- API documentation using FastAPI Swagger UI

---

# Project Structure

```text
EduGenie/
│
├── main.py
├── gemini_client.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── schemas.py
├── requirements.txt
├── requirements-local.txt
├── .env
├── .env.example
├── .gitignore
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
└── tests/
    └── test_app.py
