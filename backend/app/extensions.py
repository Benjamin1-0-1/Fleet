from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

# shared singletons
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
