# Project Review Website

A full-stack starter implementation of the **Project Review Website** described in the uploaded summary. It includes:

- **Frontend:** Vue 3 + Vite
- **Backend:** Django REST Framework
- **Microservice:** Flask for feedback/search/helpfulness/credibility APIs
- **Database:** MySQL via Docker Compose

## Features implemented

- User registration/login with JWT and roles (`presenter`, `reviewer`, `admin`)
- Project creation, update, listing, detail view
- File upload path or video URL storage
- Search logs
- Ratings with per-project aggregates
- Collaboration membership records
- Helpful / not helpful feedback signals
- Reviewer credibility score
- Top reviewers leaderboard
- Basic moderation report model and APIs

## Quickest way to run

### 1) Prerequisites
- Docker Desktop
- Git (optional)

### 2) Start everything
```bash
docker compose up --build
```

### 3) Open the apps
- Frontend: http://localhost:5173
- Django API: http://localhost:8000/api/
- Flask service: http://localhost:5000/
- Django admin: http://localhost:8000/admin/

### 4) Create the admin user
In a new terminal:
```bash
docker compose exec django python manage.py makemigrations
docker compose exec django python manage.py migrate
docker compose exec django python manage.py createsuperuser
```

### 5) Seed demo data (optional)
```bash
docker compose exec django python manage.py seed_demo
```

## Local non-Docker run
See the `docs/run-without-docker.md` file.
