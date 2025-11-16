# Post-Conversation Analysis – Django REST API

This project was built as part of the Kipps.AI Internship Assignment.  
It analyzes conversations between users and AI agents, generates multiple quality and interaction metrics, and stores the results in a database for reporting.

A preconfigured **SQLite database is included**, so the project runs immediately after installation.  
No additional setup is required to generate or view data.

---

## 🚀 Features
- Upload chat conversations in JSON format  
- Analyze conversations based on clarity, relevance, completeness, sentiment, empathy, resolution, fallback detection, and more  
- Store messages and analysis results in the database  
- API endpoints for uploading, analyzing, and listing reports  
- Admin dashboard for managing data  
- Optional Celery + Celery Beat support for daily scheduled analysis  

---

## 🔐 Admin Access

A ready-to-use admin account is included:

- **Username:** admin  
- **Email:** admin@example.com  
- **Password:** password123  

---

## 📥 Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate         # Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Apply migrations (database already setup, but safe to run):

```bash
python manage.py migrate
```

4. Start development server:

```bash
python manage.py runserver
```

---

## ▶️ Running the Application

Start the API server:

```bash
python manage.py runserver
```

API Base URL:

```
http://127.0.0.1:8000/api/
```

Admin Panel:

```
http://127.0.0.1:8000/admin/
```

---

## 📡 API Endpoints

### **POST /api/conversations/**

Upload a chat conversation.

**Request:**

```json
{
  "messages": [
    {"sender": "user", "message": "Hi, I need help."},
    {"sender": "ai", "message": "Sure, how can I assist you?"}
  ]
}
```

**Response:**

```json
{
  "conversation_id": 1
}
```

---

### **POST /api/analyse/**

Analyze a conversation.

**Request:**

```json
{
  "conversation_id": 1
}
```

**Response Example:**

```json
{
  "id": 1,
  "conversation": 1,
  "clarity_score": 0.85,
  "relevance_score": 0.70,
  "accuracy_score": 0.75,
  "completeness_score": 0.80,
  "sentiment": "positive",
  "empathy_score": 0.67,
  "avg_response_time": 2.5,
  "resolved": true,
  "escalation_needed": false,
  "fallback_count": 0,
  "overall_score": 0.76,
  "created_at": "2025-11-16T12:00:00Z"
}
```

---

### **GET /api/reports/**

Get all stored analysis reports.

**Response Example:**

```json
[
  {
    "id": 1,
    "conversation": 1,
    "clarity_score": 0.85,
    "relevance_score": 0.70,
    "accuracy_score": 0.75
  }
]
```

---

## 🧠 Analysis Parameters

The system computes the following metrics:

* Clarity Score
* Relevance Score
* Accuracy Score
* Completeness Score
* Sentiment
* Empathy Score
* Average Response Time
* Resolved
* Escalation Needed
* Fallback Count
* Overall Score

---

## 🗃️ Database

The SQLite database (`db.sqlite3`) is included in the repository.
All models and tables are already configured.

Models:

* **Conversation** – stores conversation metadata
* **Message** – stores individual messages
* **ConversationAnalysis** – stores analysis results

---

## ⏱️ Celery Setup (Optional)

This project supports optional daily scheduled analysis using Celery + Redis.

Start Redis:

```bash
redis-server
```

Start Celery worker:

```bash
celery -A kipps_ai worker --loglevel=info
```

Start Celery Beat:

```bash
celery -A kipps_ai beat --loglevel=info
```

Manual command:

```bash
python manage.py analyze_conversations
```

---

## 🖥️ Deployment (Optional – Windows)

Run using Waitress:

```bash
pip install waitress
waitress-serve --port=8000 kipps_ai.wsgi:application
```

Or using a custom file:

```python
from waitress import serve
from kipps_ai.wsgi import application

if __name__ == "__main__":
    serve(application, host="0.0.0.0", port=8000)
```

---

## 👤 Author

Harsh Tiwari
