
from fastapi import status ,HTTPException
from sqlalchemy.orm import Session
from models import models
from schemas import admin
from utils.hashing import Hash


# from datetime import datetimedef 

def create(request  :admin.AdminSchema ,db :Session):
    new_admin = models.Admin(nom =request.nom,prenom=request.prenom, email=request.email,password = Hash.bcrypt(request.hashed_password),createdAt=request.created_at,role ='Admin')#refer to the db mosule Structure
    db.add(new_admin)   
    db.commit()
    db.refresh(new_admin)
    return new_admin

def destry(id ,db :Session ):
    db.query(models.Admin).filter(models.Admin.id == id).delete(synchronize_session=False)
    db.commit()
    return {'Admin deleted Successfuly'}

def update(id ,request :admin.AdminSchema ,db :Session):
    admin = db.query(models.Admin).filter(models.Admin.id == id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,Detail =f'the Admin with id = {id} is not available')
    
    for var, value in vars(request).items():
        if value is not None:
            setattr(admin, var, value)
    db.commit()    
    return {'Admin Updated Succefully'}
# getAll(db :Session):
#     admins = db.query(models.Admin).all()
#     return admins

def getById(id,db :Session):
    result = db.query(models.Admin).filter(models.Admin.id == id).first()
    if not result : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,Detail =f'Admin with this id = {id} is not available')
    return result


# getAll Avo:
def getAll(db :Session):
    admins = db.query(models.Admin).all()
    return admins


def get_Avocat_by_email(db: Session, email: str):
    avocat = db.query(models.Avocat).filter(models.Avocat.email == email).first()
    if not avocat : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,Detail =f'Avocat with this email = {email} is not available')
    return avocat


def get_Non_validate_Avos(db: Session):
    unvalidated_showavocats = db.query(models.Avocat).filter(models.Avocat.is_validate == False).all()
    return unvalidated_showavocats
def get_validate_Avos(db: Session):
    validated_showavocats = db.query(models.Avocat).filter(models.Avocat.is_validate == True).all()
    return validated_showavocats

def validate(db: Session, email: str):
    avocat = db.query(models.Avocat).filter(models.Avocat.email == email).first()
    if avocat.is_validate : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,Detail ="this profile is allredy validated")
    # if avocat is None:
    #     raise HTTPException(status_code=404, detail="Avocat not found")
    avocat.is_validate = True
    db.commit()
    return {"detail": f"Avocat {email} has been validated"}

def destroyAvo(db: Session, email: str):
    db.query(models.Avocat).filter(models.Avocat.email == email).delete(synchronize_session=False)
    db.commit()
    return {'avocat deleted Successfuly'}