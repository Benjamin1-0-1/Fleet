"""Holds singletons so they can be imported anywhere without circular issues."""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()      # ORM
migrate = Migrate()
