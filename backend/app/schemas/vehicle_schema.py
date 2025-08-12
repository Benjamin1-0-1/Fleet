from ..extensions import ma
from ..models.vehicle import Vehicle

class VehicleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vehicle
        load_instance = True

vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)
