# backend/app.py

from flask import Flask
from flask_restx import Api
from config import Config
from extensions import db
from backend.routes.vehicle_routes import fleets_ns
from backend.routes.client_routes import clients_ns
from backend.routes.reminder_routes import reminders_ns
from backend.routes.analytics_routes import analytics_ns

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    api = Api(
        app,
        version="1.0",
        title="MyFleet Performance API",
        description="Vehicle, Client, Reminder & Analytics endpoints",
        doc="/docs"
    )

    api.add_namespace(fleets_ns)
    api.add_namespace(clients_ns)
    api.add_namespace(reminders_ns)
    api.add_namespace(analytics_ns)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
