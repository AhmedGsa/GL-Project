from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer
from config.db import get_db
from sqlalchemy.orm import Session
from schemas.auth import UserRegisterSchema, LoginSchema, AvocatRegisterSchema
from repositories import user, avocat
from models.models import Role
from utils.jwt import JWT
from utils.hashing import Hash
from typing import Annotated
from config.google import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URL
import requests

bearer_scheme = HTTPBearer()

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

@router.get("/login/google")
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URL}&scope=openid%20profile%20email&access_type=offline"
    }

@router.get("/redirect")
async def auth_google(code: str, db: Session = Depends(get_db)):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URL,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token")
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    user_info = user_info.json()
    # create user if not exists
    userExists = user.get_by_email(db, user_info["email"])
    if not userExists:
        newUser = user.create(db, UserRegisterSchema(email=user_info["email"], nom=user_info["family_name"], prenom=user_info["given_name"]))
        token = JWT.create_token({"id": newUser.id, "email": newUser.email, "role": f"{newUser.role}"})
        return {"token": token}
    token = JWT.create_token({"id": userExists.id, "email": userExists.email, "role": f"{userExists.role}"})
    return RedirectResponse(f"http://localhost:5173/login?token={token}")

@router.post("/register-user")
def register_user(userRegisterSchema: UserRegisterSchema, db: Session = Depends(get_db)):
    userExists = user.get_by_email(db, userRegisterSchema.email)
    if userExists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already used")
    newUser = user.create(db, userRegisterSchema)
    token = JWT.create_token({"id": newUser.id, "email": newUser.email})
    return {"token": token}

@router.post("/register-avocat")
def register_avocat(image: UploadFile, address: Annotated[str, Form()],wilaya:Annotated[str, Form()], phoneNumber: Annotated[str, Form()], facebookUrl: Annotated[str, Form()], description: Annotated[str, Form()], categories: Annotated[str, Form()], workDays: Annotated[str, Form()], availabilityIds: Annotated[str, Form()], email: Annotated[str, Form()], password: Annotated[str, Form()], nom: Annotated[str, Form()], prenom: Annotated[str, Form()], longitude: Annotated[str, Form()], latitude: Annotated[str, Form()], db: Session = Depends(get_db)):
    avocatRegisterSchema = AvocatRegisterSchema(email=email, password=password, nom=nom, prenom=prenom, address=address,wilaya = wilaya, phoneNumber=phoneNumber, facebookUrl=facebookUrl, description=description, categories=categories.split(","),longitude=float(longitude), latitude=float(latitude), workDays=workDays.split(","), availabilityIds=availabilityIds.split(","))
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

@router.get("/me")
def get_me(request: Request, db: Session = Depends(get_db), token: str = Depends(bearer_scheme)):
    userId = request.state.user["id"]
    userExists = user.get_by_id(db, userId)
    if not userExists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    print(userExists.role)
    if userExists.role == Role.avocat:
        avocatExists = avocat.get_by_user_id(db, userId)
        return {
            "id": userExists.id,
            "nom": userExists.nom,
            "prenom": userExists.prenom,
            "email": userExists.email,
            "role": userExists.role,
            "imageUrl": avocatExists.imageUrl,
        }
    return {
        "id": userExists.id,
        "nom": userExists.nom,
        "prenom": userExists.prenom,
        "email": userExists.email,
        "role": userExists.role,
    }