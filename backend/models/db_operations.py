from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from typing import List, Optional
from database.models import Technician, ServiceArea, Specialty, AvailabilitySlot, Appointment, CallLog


class DBOperations:

    def get_all_technicians(self, db: Session) -> List[Technician]:
        return db.query(Technician).filter(Technician.is_active == True).options(
            joinedload(Technician.service_areas),
            joinedload(Technician.specialties),
            joinedload(Technician.availability_slots),
        ).all()

    def get_technician_by_id(self, db: Session, technician_id: int) -> Optional[Technician]:
        return db.query(Technician).filter(Technician.id == technician_id).options(
            joinedload(Technician.service_areas),
            joinedload(Technician.specialties),
            joinedload(Technician.availability_slots),
        ).first()

    def find_matching_technicians(self, db: Session, zip_code: str, appliance_type: str) -> List[Technician]:
        """Find technicians that serve a zip code and handle the appliance type."""
        appliance_lower = appliance_type.lower().strip()

        technicians = (
            db.query(Technician)
            .join(Technician.service_areas)
            .join(Technician.specialties)
            .filter(
                and_(
                    Technician.is_active == True,
                    ServiceArea.zip_code == zip_code,
                    Specialty.appliance_type.ilike(f"%{appliance_lower}%"),
                )
            )
            .options(
                joinedload(Technician.service_areas),
                joinedload(Technician.specialties),
                joinedload(Technician.availability_slots),
            )
            .distinct()
            .all()
        )
        return technicians


    def get_available_slots(self, db: Session, technician_id: int) -> List[AvailabilitySlot]:
        return (
            db.query(AvailabilitySlot)
            .filter(
                and_(
                    AvailabilitySlot.technician_id == technician_id,
                    AvailabilitySlot.is_booked == False,
                )
            )
            .all()
        )

    def mark_slot_booked(self, db: Session, slot_id: int) -> Optional[AvailabilitySlot]:
        slot = db.query(AvailabilitySlot).filter(AvailabilitySlot.id == slot_id).first()
        if slot:
            slot.is_booked = True
            db.commit()
            db.refresh(slot)
        return slot


    def create_appointment(self, db: Session, data: dict) -> Appointment:
        appt = Appointment(**data)
        db.add(appt)
        db.commit()
        db.refresh(appt)
        return appt

    def get_all_appointments(self, db: Session) -> List[Appointment]:
        return (
            db.query(Appointment)
            .options(joinedload(Appointment.technician))
            .order_by(Appointment.created_at.desc())
            .all()
        )

    def get_appointment_by_id(self, db: Session, appt_id: int) -> Optional[Appointment]:
        return db.query(Appointment).filter(Appointment.id == appt_id).options(
            joinedload(Appointment.technician)
        ).first()

    def update_appointment_status(self, db: Session, appt_id: int, status: str) -> Optional[Appointment]:
        appt = db.query(Appointment).filter(Appointment.id == appt_id).first()
        if appt:
            appt.status = status
            db.commit()
            db.refresh(appt)
        return appt


    def create_call_log(self, db: Session, call_id: str, caller_phone: Optional[str] = None) -> CallLog:
        log = CallLog(call_id=call_id, caller_phone=caller_phone)
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    def get_call_log(self, db: Session, call_id: str) -> Optional[CallLog]:
        return db.query(CallLog).filter(CallLog.call_id == call_id).first()

    def update_call_log(self, db: Session, call_id: str, updates: dict) -> Optional[CallLog]:
        log = db.query(CallLog).filter(CallLog.call_id == call_id).first()
        if log:
            for key, value in updates.items():
                if value is not None:
                    setattr(log, key, value)
            db.commit()
            db.refresh(log)
        return log

    def get_all_call_logs(self, db: Session) -> List[CallLog]:
        return db.query(CallLog).order_by(CallLog.started_at.desc()).all()

    def get_live_call_logs(self, db: Session) -> List[CallLog]:
        """Return only calls currently in-progress."""
        return (
            db.query(CallLog)
            .filter(CallLog.status == "in-progress")
            .order_by(CallLog.started_at.desc())
            .all()
        )

    def delete_all_calls(self, db: Session) -> int:
        deleted = db.query(CallLog).delete()
        db.commit()
        return deleted
