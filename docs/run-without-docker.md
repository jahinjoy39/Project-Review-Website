# Run Without Docker

## Requirements
- Python 3.11+
- Node.js 20+
- MySQL 8+

## 1) Create MySQL database
Create a database named `projectreview`.

## 2) Run Django
```bash
cd backend-django
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 3) Run Flask
```bash
cd flask-service
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

## 4) Run Vue frontend
```bash
cd frontend-vue
npm install
npm run dev
```
