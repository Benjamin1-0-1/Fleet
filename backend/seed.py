from datetime import date
from app import create_app
from app.extensions import db
from app.models.vehicle import Vehicle
from app.models.client import Client
from app.models.vehicle_cost import VehicleCost
from app.models.client_rating import ClientRating
from app.models.reminder import Reminder

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    v1 = Vehicle(plate="KAB-123A", make="Toyota", model="Corolla", colour="White", v_class="sedan", purchase_price=8000)
    v2 = Vehicle(plate="KCD-456B", make="Nissan", model="Navara", colour="Silver", v_class="truck", purchase_price=15000)

    c1 = Client(first_name="Alice", last_name="Nduta", email="alice@example.com", phone="0712123123", address="Nairobi")
    c2 = Client(first_name="Bob", last_name="Mutua", email="bob@example.com", phone="0722456456", address="Mombasa")

    db.session.add_all([v1, v2, c1, c2])
    db.session.flush()  # <-- ensures v1.id / v2.id / c1.id exist without committing

    cost1 = VehicleCost(vehicle_id=v1.id, cost_type="fuel", amount=85)
    cost2 = VehicleCost(vehicle_id=v2.id, cost_type="repair", amount=230)

    r1 = ClientRating(client_id=c1.id, stars=5, feedback="Prompt payer")
    r2 = ClientRating(client_id=c2.id, stars=3, feedback="Late return once")

    rem1 = Reminder(vehicle_id=v1.id, reminder_type="service", due_date=date(2025, 9, 1))

    db.session.add_all([cost1, cost2, r1, r2, rem1])
    db.session.commit()

    print("🌱 Seeded!")
