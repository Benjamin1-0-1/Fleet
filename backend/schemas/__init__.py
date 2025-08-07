from .vehicle_schema import vehicle_schema, vehicles_schema
from .vehicle_cost_schema import vehicle_cost_schema, vehicle_costs_schema
from .vehicle_status_history_schema import (
    vehicle_status_history_schema,
    vehicle_status_history_schemas,
)
from .client_schema import client_schema, clients_schema
from .client_rating_schema import client_rating_schema, client_ratings_schema
from .reminder_schema import reminder_schema, reminders_schema

__all__ = [
    # vehicles
    "vehicle_schema",
    "vehicles_schema",
    "vehicle_cost_schema",
    "vehicle_costs_schema",
    "vehicle_status_history_schema",
    "vehicle_status_history_schemas",
    # clients
    "client_schema",
    "clients_schema",
    "client_rating_schema",
    "client_ratings_schema",
    # reminders
    "reminder_schema",
    "reminders_schema",
]
