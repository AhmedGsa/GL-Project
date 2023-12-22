from fastapi import APIRouter, Depends, status, HTTPException
from config.db import get_db
from sqlalchemy.orm import Session
from schemas.auth import UserRegisterSchema, LoginSchema,AvocatRegisterSchema
from repositories import admin,avocat , user
from utils.jwt import JWT
from utils.hashing import Hash

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login(loginSchema: LoginSchema, db: Session = Depends(get_db)):
    userExists = user.get_by_email(db, loginSchema.email)
    if not userExists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not Hash.compare(userExists.password, loginSchema.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    token = JWT.create_token({"id": userExists.id, "email": userExists.email})
    return {"token": token}


@router.post("/register-avocat")
async def register_user(request: AvocatRegisterSchema, db: Session = Depends(get_db)):
    userExists = avocat.get_avocat_by_email(db, request.email)
    if userExists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already used")
    return avocat.create(db, request)
    # token = JWT.create_token({"id": newUser.id, "email": newUser.email})
    # return {"token": token}

@router.post("/register-user")
async def register_user(userRegisterSchema: UserRegisterSchema, db: Session = Depends(get_db)):
    userExists = user.get_by_email(db, userRegisterSchema.email)
    if userExists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already used")
    newUser = user.create(db, userRegisterSchema)
    token = JWT.create_token({"id": newUser.id, "email": newUser.email})
    return {"token": token}

