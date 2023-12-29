from fastapi import APIRouter, Depends, Request, status, HTTPException
from config.db import get_db
from repositories.availabilities import get_all

router = APIRouter(prefix="/availability", tags=["Availability"])

@router.get("/all")
def get_all_availabilities(db = Depends(get_db)):
    return get_all(db)