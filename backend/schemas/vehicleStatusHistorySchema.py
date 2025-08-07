from ..extensions import ma
from ..models.vehicleStatusHistory import VehicleStatusHistory


class VehicleStatusHistorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VehicleStatusHistory
        load_instance = True


vehicle_status_history_schema  = VehicleStatusHistorySchema()
vehicle_status_history_schemas = VehicleStatusHistorySchema(many=True)
