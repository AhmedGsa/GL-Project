from fastapi import status ,HTTPException
from sqlalchemy.orm import Session
from models import models
from schemas import avocat
from utils.hashing import Hash


def Avocatcreate(request :avocat.AvocatSchema,db: Session):
    new_avocat = models.Avocat(name= request.name,fname = request.fname,email = request.email,password = Hash.bcrypt(request.password),createdAt=request.createdAt,role = "Avocat",adress =request.adress,is_validate=False,phoneNumber = request.phoneNumber,facebookUrl = request.facebookUrl,description = request.description)
    db.add(new_avocat)
    db.commit()
    db.refresh(new_avocat)
    return new_avocat

def get_by_email(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user


def get_avocat_by_email(db: Session, email: str):
    avocat = db.query(models.Avocat).filter(models.Avocat.email == email).first()
    return avocat