from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.models import Appointment, Availability
from schemas.appointment import CreateAppointmentSchema, GetAvailableAppointmentTimesSchema

def get_all(db: Session):
    availabilites = db.query(Appointment).all()
    return availabilites

def create(db: Session, createAppointmentSchema: CreateAppointmentSchema, userId: int):
    isAvailable = db.query(Appointment).filter(Appointment.availabilityId == createAppointmentSchema.availabilityId, Appointment.date == createAppointmentSchema.date).first()
    if isAvailable:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Appointment is booked")
    newAppointment = Appointment(userId=userId, **createAppointmentSchema.model_dump())
    db.add(newAppointment)
    db.commit()
    db.refresh(newAppointment)
    return newAppointment

def get_available_times(db: Session, avocatId: int, date: str):
    bookedAppointments = db.query(Appointment).filter(Appointment.avocatId == avocatId, Appointment.date == date).all()
    availabilities = db.query(Availability).filter(Availability.id.not_in([appointment.availabilityId for appointment in bookedAppointments])).all()
    return availabilities