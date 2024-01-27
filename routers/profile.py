from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from repositories import user, avocat
from models.models import Role
from config.db import get_db
from schemas.auth import AvocatRegisterSchema
from utils.hashing import Hash
from schemas.profile import ChangePassword


bearer_scheme = HTTPBearer()

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.patch("/update")
def update_user(request: Request, address: Annotated[str, Form()], wilaya:Annotated[str, Form()], phoneNumber: Annotated[str, Form()], facebookUrl: Annotated[str, Form()], description: Annotated[str, Form()], categories: Annotated[str, Form()], workDays: Annotated[str, Form()], availabilityIds: Annotated[str, Form()], email: Annotated[str, Form()], nom: Annotated[str, Form()], prenom: Annotated[str, Form()], longitude: Annotated[str, Form()], latitude: Annotated[str, Form()], image: UploadFile = None, db: Session = Depends(get_db), token: str = Depends(bearer_scheme)):
    userId = request.state.user["id"]
    avocatRegisterSchema = AvocatRegisterSchema(email=email, nom=nom, prenom=prenom, address=address,Wilaya = wilaya, phoneNumber=phoneNumber, facebookUrl=facebookUrl, description=description, categories=categories.split(","),longitude=float(longitude), latitude=float(latitude), workDays=workDays.split(","), availabilityIds=availabilityIds.split(","))
    userExists = user.get_by_email(db, avocatRegisterSchema.email)
    if userExists.role != Role.avocat:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not an avocat")
    if userExists and userExists.id != userId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already used")
    user.update(db, userId, avocatRegisterSchema)
    if image:
        try:
            contents = image.file.read()
            fileExt = image.filename.split(".")[-1]
            with open(f"./uploads/{userId}.{fileExt}", 'wb') as f:
                f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the file"}
        finally:
            image.file.close()
    avocat.update(db, userId, {"userId": userId, **avocatRegisterSchema.model_dump(), "imageUrl": f"http://localhost:8000/avocat/image/{userId}.{fileExt}" if image else None})
    return {"message": "Profile updated successfully"}

@router.post("/change-password")
def change_password(request: Request, changePasswordSchema: ChangePassword, db: Session = Depends(get_db), token: str = Depends(bearer_scheme)):
    userId = request.state.user["id"]
    userExists = user.get_by_id(db, userId)
    if not userExists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not Hash.compare(userExists.password, changePasswordSchema.oldPassword):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is incorrect")
    user.update_password(db, userId, changePasswordSchema.newPassword)
    return {"message": "Password updated successfully"}