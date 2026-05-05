"""
Seed the database with sample technicians, service areas, specialties, and availability.
Run: python scripts/seed_data.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend"))

from database.connection import Base, engine
from database.session import SessionLocal
from database.models import Technician, ServiceArea, Specialty, AvailabilitySlot

TECHNICIANS = [
    {
        "name": "Carlos Rivera",
        "email": "carlos.rivera@fixpro.com",
        "phone": "+1-555-201-0001",
        "zip_codes": ["90210", "90211", "90212"],
        "specialties": ["washer", "dryer", "dishwasher"],
        "slots": [
            {"day": "Monday",    "date": "2025-07-07", "start": "09:00", "end": "12:00"},
            {"day": "Monday",    "date": "2025-07-07", "start": "14:00", "end": "17:00"},
            {"day": "Wednesday", "date": "2025-07-09", "start": "10:00", "end": "13:00"},
            {"day": "Friday",    "date": "2025-07-11", "start": "09:00", "end": "12:00"},
        ],
    },
    {
        "name": "Priya Nair",
        "email": "priya.nair@fixpro.com",
        "phone": "+1-555-201-0002",
        "zip_codes": ["10001", "10002", "10003"],
        "specialties": ["refrigerator", "oven", "dishwasher"],
        "slots": [
            {"day": "Tuesday",   "date": "2025-07-08", "start": "08:00", "end": "11:00"},
            {"day": "Tuesday",   "date": "2025-07-08", "start": "13:00", "end": "16:00"},
            {"day": "Thursday",  "date": "2025-07-10", "start": "10:00", "end": "14:00"},
            {"day": "Saturday",  "date": "2025-07-12", "start": "09:00", "end": "12:00"},
        ],
    },
    {
        "name": "James Whitfield",
        "email": "james.whitfield@fixpro.com",
        "phone": "+1-555-201-0003",
        "zip_codes": ["60601", "60602", "60603", "60604"],
        "specialties": ["hvac", "oven", "washer"],
        "slots": [
            {"day": "Monday",    "date": "2025-07-07", "start": "10:00", "end": "14:00"},
            {"day": "Wednesday", "date": "2025-07-09", "start": "08:00", "end": "12:00"},
            {"day": "Friday",    "date": "2025-07-11", "start": "13:00", "end": "17:00"},
        ],
    },
    {
        "name": "Angela Moss",
        "email": "angela.moss@fixpro.com",
        "phone": "+1-555-201-0004",
        "zip_codes": ["77001", "77002", "77003"],
        "specialties": ["refrigerator", "washer", "dryer"],
        "slots": [
            {"day": "Monday",    "date": "2025-07-07", "start": "08:00", "end": "11:00"},
            {"day": "Thursday",  "date": "2025-07-10", "start": "09:00", "end": "13:00"},
            {"day": "Friday",    "date": "2025-07-11", "start": "10:00", "end": "14:00"},
        ],
    },
    {
        "name": "Derek Okafor",
        "email": "derek.okafor@fixpro.com",
        "phone": "+1-555-201-0005",
        "zip_codes": ["30301", "30302", "30303"],
        "specialties": ["hvac", "dryer", "dishwasher"],
        "slots": [
            {"day": "Tuesday",   "date": "2025-07-08", "start": "09:00", "end": "12:00"},
            {"day": "Wednesday", "date": "2025-07-09", "start": "13:00", "end": "17:00"},
            {"day": "Saturday",  "date": "2025-07-12", "start": "08:00", "end": "12:00"},
        ],
    },
    {
        "name": "Sofia Hernandez",
        "email": "sofia.hernandez@fixpro.com",
        "phone": "+1-555-201-0006",
        "zip_codes": ["85001", "85002", "85003", "85004"],
        "specialties": ["oven", "refrigerator", "hvac"],
        "slots": [
            {"day": "Monday",    "date": "2025-07-07", "start": "11:00", "end": "15:00"},
            {"day": "Tuesday",   "date": "2025-07-08", "start": "08:00", "end": "12:00"},
            {"day": "Thursday",  "date": "2025-07-10", "start": "14:00", "end": "17:00"},
        ],
    },
    {
        "name": "Marcus Lee",
        "email": "marcus.lee@fixpro.com",
        "phone": "+1-555-201-0007",
        "zip_codes": ["98101", "98102", "98103"],
        "specialties": ["washer", "dryer", "hvac"],
        "slots": [
            {"day": "Monday",    "date": "2025-07-07", "start": "09:00", "end": "13:00"},
            {"day": "Wednesday", "date": "2025-07-09", "start": "09:00", "end": "12:00"},
            {"day": "Friday",    "date": "2025-07-11", "start": "08:00", "end": "11:00"},
        ],
    },
    {
        "name": "Fatima Al-Rashid",
        "email": "fatima.alrashid@fixpro.com",
        "phone": "+1-555-201-0008",
        "zip_codes": ["48201", "48202", "48203"],
        "specialties": ["dishwasher", "refrigerator", "oven"],
        "slots": [
            {"day": "Tuesday",   "date": "2025-07-08", "start": "10:00", "end": "14:00"},
            {"day": "Thursday",  "date": "2025-07-10", "start": "09:00", "end": "12:00"},
            {"day": "Saturday",  "date": "2025-07-12", "start": "10:00", "end": "14:00"},
        ],
    },
    {
        "name": "Ethan Brooks",
        "email": "ethan.brooks@fixpro.com",
        "phone": "+1-555-201-0009",
        "zip_codes": ["02101", "02102", "02103", "02110"],
        "specialties": ["washer", "refrigerator", "dishwasher", "hvac"],
        "slots": [
            {"day": "Monday",    "date": "2025-07-07", "start": "13:00", "end": "17:00"},
            {"day": "Wednesday", "date": "2025-07-09", "start": "14:00", "end": "17:00"},
            {"day": "Friday",    "date": "2025-07-11", "start": "12:00", "end": "16:00"},
        ],
    },
    {
        "name": "Linda Zhao",
        "email": "linda.zhao@fixpro.com",
        "phone": "+1-555-201-0010",
        "zip_codes": ["94102", "94103", "94105", "90210"],
        "specialties": ["dryer", "oven", "washer", "dishwasher"],
        "slots": [
            {"day": "Tuesday",   "date": "2025-07-08", "start": "08:00", "end": "11:00"},
            {"day": "Thursday",  "date": "2025-07-10", "start": "08:00", "end": "12:00"},
            {"day": "Saturday",  "date": "2025-07-12", "start": "13:00", "end": "17:00"},
        ],
    },
]


def seed():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Clear existing data
        db.query(AvailabilitySlot).delete()
        db.query(Specialty).delete()
        db.query(ServiceArea).delete()
        db.query(Technician).delete()
        db.commit()

        for t_data in TECHNICIANS:
            tech = Technician(
                name=t_data["name"],
                email=t_data["email"],
                phone=t_data["phone"],
            )
            db.add(tech)
            db.flush()  # Get the ID

            for zip_code in t_data["zip_codes"]:
                db.add(ServiceArea(technician_id=tech.id, zip_code=zip_code))

            for appliance in t_data["specialties"]:
                db.add(Specialty(technician_id=tech.id, appliance_type=appliance))

            for slot in t_data["slots"]:
                db.add(AvailabilitySlot(
                    technician_id=tech.id,
                    day_of_week=slot["day"],
                    date=slot["date"],
                    start_time=slot["start"],
                    end_time=slot["end"],
                    is_booked=False,
                ))

        db.commit()
        print(f"✅ Seeded {len(TECHNICIANS)} technicians successfully.")
    except Exception as e:
        db.rollback()
        print(f"❌ Seeding failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
