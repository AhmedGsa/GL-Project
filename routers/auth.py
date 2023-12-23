from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile, Form
from config.db import get_db
from sqlalchemy.orm import Session
from schemas.auth import UserRegisterSchema, LoginSchema, AvocatRegisterSchema
from repositories import user, avocat
from utils.jwt import JWT
from utils.hashing import Hash
from typing import Annotated

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

@router.post("/register-user")
def register_user(userRegisterSchema: UserRegisterSchema, db: Session = Depends(get_db)):
    userExists = user.get_by_email(db, userRegisterSchema.email)
    if userExists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already used")
    newUser = user.create(db, userRegisterSchema)
    token = JWT.create_token({"id": newUser.id, "email": newUser.email})
    return {"token": token}

@router.post("/register-avocat")
def register_avocat(image: UploadFile, address: Annotated[str, Form()], phoneNumber: Annotated[str, Form()], facebookUrl: Annotated[str, Form()], description: Annotated[str, Form()], categories: Annotated[list[str], Form()], email: Annotated[str, Form()], password: Annotated[str, Form()], nom: Annotated[str, Form()], prenom: Annotated[str, Form()], db: Session = Depends(get_db)):
    avocatRegisterSchema = AvocatRegisterSchema(email=email, password=password, nom=nom, prenom=prenom, address=address, phoneNumber=phoneNumber, facebookUrl=facebookUrl, description=description, categories=categories)
    userExists = user.get_by_email(db, avocatRegisterSchema.email)
    if userExists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already used")
    newUser = user.create_avocat(db, avocatRegisterSchema)
    try:
        contents = image.file.read()
        fileExt = image.filename.split(".")[-1]
        with open(f"./uploads/{newUser.id}.{fileExt}", 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        image.file.close()
    avocat.create(db, {"userId": newUser.id, **avocatRegisterSchema.model_dump(), "imageUrl": f"http://localhost:8000/avocat/image/{newUser.id}.{fileExt}"})
    token = JWT.create_token({"id": newUser.id, "email": newUser.email})
    return {"token": token}