from fastapi import APIRouter, Depends, Request, status, HTTPException
from schemas.appointment import CreateAppointmentSchema, GetAvailableAppointmentTimesSchema
from repositories import appointment
from fastapi.security import HTTPBearer
from config.db import get_db
from utils.jwt import JWT

router = APIRouter(prefix="/appointment", tags=["Appointment"])

bearer_scheme = HTTPBearer()

@router.post("/create")
def create_appointment(request: Request, createAppointmentSchema: CreateAppointmentSchema, token: str = Depends(bearer_scheme), db = Depends(get_db)):
    appointment.create(db, createAppointmentSchema, request.state.user["id"])
    return {"message": "appointment created"}

@router.get("/available-times")
def get_available_times(avocatId: int, date: str, db = Depends(get_db)):
    return appointment.get_available_times(db, avocatId, date)

@router.get("/avocat-appointments")
def get_avocat_appointments(request: Request, db = Depends(get_db), token: str = Depends(bearer_scheme)):
    return appointment.get_avocat_appointments(db, request.state.user["id"])

@router.patch("/mark-as-done/{appointmentId}")
def mark_as_done(request: Request, appointmentId: int, db = Depends(get_db), token: str = Depends(bearer_scheme)):
    appointment.mark_as_done(db, appointmentId, request.state.user["id"])
    return {"message": "appointment marked as done !"}

@router.patch("/mark-as-canceled/{appointmentId}")
def mark_as_canceled(request: Request, appointmentId: int, db = Depends(get_db), token: str = Depends(bearer_scheme)):
    appointment.mark_as_canceled(db, appointmentId, request.state.user["id"])
    return {"message": "appointment marked as canceled !"}
