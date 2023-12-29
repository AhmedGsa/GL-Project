from sqlalchemy.orm import Session
from models.models import Appointment
from schemas.appointment import CreateAppointmentSchema

def get_all(db: Session):
    availabilites = db.query(Appointment).all()
    return availabilites

def create(db: Session, createAppointmentSchema: CreateAppointmentSchema, userId: int):
    newAppointment = Appointment(userId=userId, **createAppointmentSchema.model_dump())
    db.add(newAppointment)
    db.commit()
    db.refresh(newAppointment)
    return newAppointment