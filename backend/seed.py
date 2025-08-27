from datetime import date, datetime, timedelta
import os
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.client import Client
from app.models.vehicle_cost import VehicleCost
from app.models.client_rating import ClientRating
from app.models.reminder import Reminder
from app.models.rental import Rental
from app.models.vehicle_mileage import VehicleMileage
from app.models.damage import Damage

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # demo user
    admin = User(username="admin")
    admin.set_password("admin123")
    db.session.add(admin)

    v1 = Vehicle(plate="KAB-123A", make="Toyota", model="Corolla", colour="White",
                 v_class="sedan", purchase_price=8000, image_filename="car1.jpg")
    v2 = Vehicle(plate="KCD-456B", make="Nissan", model="Navara", colour="Silver",
                 v_class="truck", purchase_price=15000, image_filename="car2.jpg")

    c1 = Client(first_name="Alice", last_name="Nduta", email="alice@example.com", phone="0712123123", address="Nairobi")
    c2 = Client(first_name="Bob", last_name="Mutua", email="bob@example.com", phone="0722456456", address="Mombasa")

    db.session.add_all([admin, v1, v2, c1, c2])
    db.session.flush()

    # mileage logs
    db.session.add_all([
        VehicleMileage(vehicle_id=v1.id, odometer=50210),
        VehicleMileage(vehicle_id=v2.id, odometer=120340),
    ])

    # costs
    db.session.add_all([
        VehicleCost(vehicle_id=v1.id, cost_type="fuel", amount=85, remark="fuel"),
        VehicleCost(vehicle_id=v2.id, cost_type="repair", amount=230, remark="brake pads"),
        VehicleCost(vehicle_id=v1.id, cost_type="insurance", amount=400),
    ])

    # rentals (one active, one returned)
    db.session.add_all([
        Rental(vehicle_id=v1.id, client_id=c1.id, start_date=date.today()-timedelta(days=5),
               end_date=date.today()+timedelta(days=2), rate_per_day=25, returned_on=None),
        Rental(vehicle_id=v2.id, client_id=c2.id, start_date=date.today()-timedelta(days=20),
               end_date=date.today()-timedelta(days=10), rate_per_day=40, returned_on=date.today()-timedelta(days=10)),
    ])

    # ratings and reminder
    db.session.add_all([
        ClientRating(client_id=c1.id, stars=5, feedback="Prompt payer"),
        ClientRating(client_id=c2.id, stars=3, feedback="Late return once"),
        Reminder(vehicle_id=v1.id, reminder_type="service", due_date=date.today()+timedelta(days=14)),
        Reminder(vehicle_id=v1.id, reminder_type="service", due_date=date.today()+timedelta(days=7)),
        Reminder(vehicle_id=v2.id, reminder_type="inspection", due_date=date.today()+timedelta(days=30)),
        Damage(vehicle_id=v2.id, description="Scratched rear bumper", cost=120)
    ])

    db.session.commit()

    # ensure demo images exist
    uploads_dir = app.config["STATIC_UPLOADS"]
    os.makedirs(uploads_dir, exist_ok=True)
    # create tiny placeholder images if missing
    for fn in ["car1.jpg", "car2.jpg"]:
        path = os.path.join(uploads_dir, fn)
        if not os.path.exists(path):
            with open(path, "wb") as f:
                f.write(b"\xff\xd8\xff\xe0" + b"\x00"*100)  # tiny invalid jpeg placeholder (ok for demo)

    print("DB Seeded!")
