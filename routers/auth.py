from fastapi import APIRouter, Depends, status, HTTPException
from config.db import get_db
from sqlalchemy.orm import Session
from schemas.auth import UserRegisterSchema
from repositories import user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login():
    return {"message": "login"}

@router.post("/register-user")
def register_user(userRegisterSchema: UserRegisterSchema, db: Session = Depends(get_db)):
    userExists = user.get_by_email(db, userRegisterSchema.email)
    if userExists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already used")
    newUser = user.create(db, userRegisterSchema)
    return newUser