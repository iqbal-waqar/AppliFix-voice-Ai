from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from models.db_operations import DBOperations

class SchedulingInteractor:

    def find_technicians_for_call(
        self, db: Session, zip_code: str, appliance_type: str
    ) -> Dict[str, Any]:
        """
        Given a zip code and appliance type, find matching technicians
        with their available time slots. Returns structured data for Vapi tool response.
        """
        technicians = DBOperations().find_matching_technicians(db, zip_code, appliance_type)

        if not technicians:
            return {
                "found": False,
                "message": f"No technicians available for {appliance_type} in zip code {zip_code}.",
                "technicians": [],
            }

        results = []
        for tech in technicians:
            slots = DBOperations().get_available_slots(db, tech.id)
            slot_list = [
                {
                    "slot_id": s.id,
                    "day": s.day_of_week,
                    "date": s.date,
                    "start_time": s.start_time,
                    "end_time": s.end_time,
                }
                for s in slots
            ]
            results.append(
                {
                    "technician_id": tech.id,
                    "technician_name": tech.name,
                    "phone": tech.phone,
                    "available_slots": slot_list,
                }
            )

        return {
            "found": True,
            "message": f"Found {len(results)} technician(s) for {appliance_type} in {zip_code}.",
            "technicians": results,
        }

    def book_appointment_from_call(self, db: Session, data: Dict[str, Any]) -> Dict[str, Any]:
        technician = DBOperations().get_technician_by_id(db, data["technician_id"])
        if not technician:
            return {"success": False, "message": "Technician not found."}

        appt_data = {
            "technician_id": data["technician_id"],
            "customer_name": data["customer_name"],
            "customer_phone": data.get("customer_phone"),
            "customer_zip": data["customer_zip"],
            "appliance_type": data["appliance_type"],
            "issue_description": data.get("issue_description"),
            "scheduled_date": data["scheduled_date"],
            "scheduled_time": data["scheduled_time"],
            "call_id": data.get("call_id"),
            "status": "confirmed",
        }

        appointment = DBOperations().create_appointment(db, appt_data)

        # Mark the matching slot as booked
        slots = DBOperations().get_available_slots(db, data["technician_id"])
        for slot in slots:
            if slot.date == data["scheduled_date"] and slot.start_time == data["scheduled_time"]:
                DBOperations().mark_slot_booked(db, slot.id)
                break

        return {
            "success": True,
            "appointment_id": appointment.id,
            "message": (
                f"Appointment confirmed! {technician.name} will visit on "
                f"{data['scheduled_date']} at {data['scheduled_time']} "
                f"for your {data['appliance_type']} issue."
            ),
            "details": {
                "technician": technician.name,
                "date": data["scheduled_date"],
                "time": data["scheduled_time"],
                "appliance": data["appliance_type"],
                "customer": data["customer_name"],
            },
        }
