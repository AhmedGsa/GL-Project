from fastapi import APIRouter, Depends, Request, status, HTTPException
from schemas.appointment import CreateAppointmentSchema
from repositories import appointment
from fastapi.security import HTTPBearer
from config.db import get_db
from utils.jwt import JWT

router = APIRouter(prefix="/appointment", tags=["Appointment"])

bearer_scheme = HTTPBearer()

@router.post("/create")
def create_appointment(request: Request, createAppointmentSchema: CreateAppointmentSchema, token: str = Depends(bearer_scheme), db = Depends(get_db)):
    print(request.state.user)
    appointment.create(db, createAppointmentSchema, request.state.user["id"])
    return {"message": "appointment created"}