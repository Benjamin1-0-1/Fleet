from flask import Flask, jsonify
from flask_cors import CORS
from .extensions import db, ma, migrate
from .config import Config


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    # init extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # CORS for frontend
    CORS(app, resources={r"/api/*": {"origins": app.config.get("FRONTEND_ORIGIN")}})

    # register routes
    from .routes.vehicle_routes import vehicle_bp
    from .routes.vehicle_status_history_routes import status_bp
    from .routes.vehicle_cost_routes import vehicle_cost_bp
    from .routes.client_routes import client_bp
    from .routes.client_rating_routes import rating_bp
    from .routes.reminder_routes import reminder_bp
    from .routes.analytics_routes import analytics_bp

    app.register_blueprint(vehicle_bp, url_prefix="/api/vehicles")
    app.register_blueprint(status_bp, url_prefix="/api/vehicle-status-history")
    app.register_blueprint(vehicle_cost_bp, url_prefix="/api/vehicle-costs")
    app.register_blueprint(client_bp, url_prefix="/api/clients")
    app.register_blueprint(rating_bp, url_prefix="/api/client-ratings")
    app.register_blueprint(reminder_bp, url_prefix="/api/reminders")
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")

    @app.route("/")
    def health():
        return jsonify({"status": "ok"})

    return app
