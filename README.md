# FAQ API (Python + Django)📚

A robust FAQ management system built with Django REST Framework, featuring multilingual support and caching capabilities. 🌍⚡

## Overview

This FAQ API service provides a comprehensive solution for managing frequently asked questions and their answers. It supports multiple languages through Google Translate integration and implements Redis caching for improved performance.

## Tech Stack 🛠️

- **Python 3.12**: Core programming language 🐍
- **Django 5.1**: Web framework 🌐
- **Django REST Framework**: API development 💻
- **SQLite**: Database 💾
- **Redis**: Caching layer 🗃️
- **Google Translate**: Translation service 🌐
- **Docker**: Containerization 🐳
- **pytest**: Testing framework 🔍
- **flake8**: Code linting 🧹

## 📌 Features

- ✅ Create and manage FAQs.
- ✅ Multilingual support (**English, Hindi, Bengali**).
- ✅ Redis caching for better performance.
- ✅ REST API with **GET** & **POST** endpoints.
- ✅ Docker support for easy deployment.
- ✅ Unit testing with **pytest**.
- ✅ Follows **best Git practices**.

## Project Structure 🗂️

```
FAQ/
├── faq/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── Faq/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── translations
│   └── translate.py
├── .dockerignore
├── .gitignore
├── db.sqlite3
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── Pipfile
├── Pipfile.lock
├── pytest.ini
├── README.md
├── requirements.txt
└── setup.cfg
```

## Installation & Setup 🚀

### Prerequisites

Make sure you have the following installed:

- [Python 3.12+](https://www.python.org/downloads/)

### Setup Project

1. Clone the repository:

```bash
git clone https://github.com/Rana718/BharatFD_Assignment.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run migrations:

```bash
python manage.py migrate
```

4. Start the development server:

```bash
python manage.py runserver
```

## API Endpoints 📡

Base URL is `http://localhost:8000/`

### 1️⃣ Create FAQ (POST)

```http
POST /api/faqs/
```

#### Request Body (JSON)

```json
{
  "question": "What is Google?",
  "answer": "Google is a search engine and tech company."
}
```

#### Response

```json
{
  "id": 1,
  "question": "What is Google?",
  "answer": "Google is a search engine and tech company.",
  "created_at": "2025-01-31T19:54:14.478797Z",
  "updated_at": "2025-01-31T19:54:14.478797Z"
}
```

### 2️⃣ Get FAQs (GET)

```http
GET /api/faqs/
```

#### Fetch FAQs in Different Languages

- **English (default)**: `GET /api/faqs/`
- **Hindi**: `GET /api/faqs/?lang=hi`
- **Bengali**: `GET /api/faqs/?lang=bn`

#### Response for the `GET /api/faqs/?lang=hi`

```json
[
  {
    "id": 1,
    "question": "Google क्या है?",
    "answer": "Google एक खोज इंजन और टेक कंपनी है।",
    "created_at": "2025-01-31T19:54:14.478797Z",
    "updated_at": "2025-01-31T19:54:14.478797Z"
  },
  ...
]
```

### 3️⃣ Get Single FAQ (GET)

```http
GET /api/faqs/{id}/
```

#### Fetch FAQs in Different Languages

- **English (default)**: `GET /api/faqs/{id}/`
- **Hindi**: `GET /api/faqs/{id}/?lang=hi`
- **Bengali**: `GET /api/faqs/{id}/?lang=bn`

#### Response for the `GET /api/faqs/{id}/?lang=hi`

```json
{
  "id": 1,
  "question": "Google क्या है?",
  "answer": "Google एक खोज इंजन और टेक कंपनी है।",
  "created_at": "2025-01-31T19:54:14.478797Z",
  "updated_at": "2025-01-31T19:54:14.478797Z"
}
```

## Run with Docker 🐳

```bash
docker-compose up --build
```

## Test 🚨

To ensure everything is working correctly, run the test suite using the following command:

```bash
pytest faq/tests.py -v  
```
This will execute the tests and provide detailed output to confirm that all functionalities are working as expected.