from ..extensions import ma
from ..models.vehicleCost import VehicleCost


class VehicleCostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VehicleCost
        load_instance = True


vehicle_cost_schema  = VehicleCostSchema()
vehicle_costs_schema = VehicleCostSchema(many=True)
