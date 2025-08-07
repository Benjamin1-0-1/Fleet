"""Flask application factory.
Keeps global state out of the import path so tests can spin up isolated apps."""

from flask import Flask, jsonify
from .extensions import db, ma
from .config import Config


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialise DB + serializers
    db.init_app(app)
    ma.init_app(app)

    # Register blueprints (each domain in its own file)
    from .routes.vehicle_routes import vehicle_bp
    from .routes.client_routes import client_bp
    from .routes.reminder_routes import reminder_bp
    from .routes.analytics_routes import analytics_bp
    from .routes.vehicle_cost_routes import vehicle_cost_bp
    from .routes.vehicle_status_history_routes import status_bp
    from .routes.client_rating_routes import rating_bp


    app.register_blueprint(vehicle_bp,   url_prefix="/api/vehicles")
    app.register_blueprint(client_bp,    url_prefix="/api/clients")
    app.register_blueprint(reminder_bp,  url_prefix="/api/reminders")
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")
    app.register_blueprint(vehicle_cost_bp,   url_prefix="/api/vehicle-costs")
    app.register_blueprint(status_bp,         url_prefix="/api/vehicle-status-history")
    app.register_blueprint(rating_bp,         url_prefix="/api/client-ratings")

    @app.route("/")
    def root():
        # Health-check endpoint
        return jsonify({"status": "Vehicle-Management API running"}), 200

    return app
