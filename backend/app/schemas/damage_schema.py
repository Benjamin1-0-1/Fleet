from ..extensions import ma
from ..models.damage import Damage

class DamageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Damage
        load_instance = True

damage_schema = DamageSchema()
damages_schema = DamageSchema(many=True)
