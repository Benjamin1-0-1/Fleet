from flask import Flask
from flask_restx import Api
from config import Config
from extensions import db, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    import models  # IMPORTANT: so Alembic sees your models

    api = Api(app, version="1.0", title="MyFleet API", doc="/docs")
    api.add_namespace(fleets_ns)
    api.add_namespace(clients_ns)
    api.add_namespace(reminders_ns)
    api.add_namespace(analytics_ns)
    return app
