"""Holds singletons so they can be imported anywhere without circular issues."""
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()      # ORM
ma = Marshmallow()     # JSON (de)serialisation
