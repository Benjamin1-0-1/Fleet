"""Run with  `python manage.py`  (adds Flask-Migrate CLI later if needed)."""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
