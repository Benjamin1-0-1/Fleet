"""Central config;   override vars with REAL secrets in .env or deploy platform."""
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # 👉 swap `sqlite` for PostgreSQL in prod
    DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'app.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-prod")
