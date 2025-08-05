from flask import Flask
from extensions import db, jwt, migrate
from routes.vehicles import vehicles_bp
from routes.clients import clients_bp
from routes.reminders import reminders_bp
from routes.analytics import analytics_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(vehicles_bp, url_prefix='/api/vehicles')
    app.register_blueprint(clients_bp, url_prefix='/api/clients')
    app.register_blueprint(reminders_bp, url_prefix='/api/reminders')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
