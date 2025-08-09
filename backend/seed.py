"""
Quick‐and‐dirty data seeder for the Vehicle-Management API.
• Creates the tables (SQLite by default) and inserts a few demo rows.
• Safe to re-run: it **drops everything first** – DO NOT use in production DBs.
"""

from app import create_app
from extensions import db
from models.vehicle import Vehicle
from models.client import Client
from models.vehicleCost import VehicleCost
from models.clientRating import ClientRating
from models.reminder import Reminder

def run():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        # --- demo data -----------------------------------------------------
        car1 = Vehicle(
            plate="KAB-123A",
            make="Toyota",
            model="Corolla",
            colour="White",
            v_class="sedan",
            purchase_price=8000,
        )
        car2 = Vehicle(
            plate="KCD-456B",
            make="Nissan",
            model="Navara",
            colour="Silver",
            v_class="truck",
            purchase_price=15000,
        )

        alice = Client(
            first_name="Alice",
            last_name="Nduta",
            phone="+254712123123",
            email="alice@example.com",
            address="Nairobi",
        )
        bob = Client(
            first_name="Bob",
            last_name="Mutua",
            phone="+254722456456",
            email="bob@example.com",
            address="Mombasa",
        )

        cost1 = VehicleCost(vehicle=car1, cost_type="fuel", amount=85)
        cost2 = VehicleCost(vehicle=car2, cost_type="repair", amount=230)

        rating1 = ClientRating(client=alice, stars=5, feedback="Prompt payer")
        rating2 = ClientRating(client=bob, stars=3, feedback="Late return once")

        reminder1 = Reminder(vehicle=car1, reminder_type="service", due_date="2025-09-01")

        db.session.add_all(
            [car1, car2, alice, bob, cost1, cost2, rating1, rating2, reminder1]
        )
        db.session.commit()
        # -------------------------------------------------------------------

        print("🌱  Seed complete – demo data inserted.")

if __name__ == "__main__":
    run()
