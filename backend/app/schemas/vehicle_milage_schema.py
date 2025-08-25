from ..extensions import ma
from ..models.vehicle_mileage import VehicleMileage

class VehicleMileageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VehicleMileage
        load_instance = True

mileage_schema = VehicleMileageSchema()
mileages_schema = VehicleMileageSchema(many=True)
