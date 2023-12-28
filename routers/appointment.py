from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.security import HTTPBearer
from config.db import get_db
from utils.jwt import JWT

router = APIRouter(prefix="/appointment", tags=["Appointment"])

bearer_scheme = HTTPBearer()

@router.post("/create")
def create_appointment(token: str = Depends(bearer_scheme)):
    return {"message": "appointment created"}