# Vehicle Management Web App

A full-stack web application for managing a fleet of vehicles, clients, costs, reminders, and analytics.

- **Backend:** Flask + SQLAlchemy + Marshmallow + Flask-Migrate + Flask-CORS
- **Frontend:** React (Create React App) + React Router + Axios + TailwindCSS
- **Database:** SQLite (default, easily switchable to Postgres/MySQL)

---

## 📂 Project Structure

vehicle-management/
├── backend/ # Flask API
│ ├── app/ # source code
│ │ ├── models/ # SQLAlchemy models
│ │ ├── schemas/ # Marshmallow schemas
│ │ ├── routes/ # API routes (CRUD + analytics)
│ │ ├── extensions.py # db, migrate, ma singletons
│ │ └── config.py # configuration
│ ├── seed.py # seeds demo data
│ ├── app.py # WSGI entry
│ └── requirements.txt
└── frontend/
└── client/ # CRA frontend
├── src/ # React source
│ ├── api/ # Axios API helper
│ ├── pages/ # Dashboard, Vehicles, Clients, Reminders
│ ├── components/ # Reusable UI
│ └── styles/ # Tailwind base/theme
├── package.json
└── tailwind.config.js


---

## 🚀 Backend Setup

1. Create and activate a virtualenv:

```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt


Configure environment:

cp .env.example .env   # or copy manually on Windows


Run migrations:
set FLASK_APP=app:create_app   # Windows PowerShell
# export FLASK_APP=app:create_app   # macOS/Linux

flask db init
flask db migrate -m "initial schema"
flask db upgrade
(Optional) Seed demo data:


Copy
Edit
python seed.py
Start backend:
python app.py
# API runs at http://localhost:5000
