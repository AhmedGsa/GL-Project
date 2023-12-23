
from fastapi import status ,HTTPException
from sqlalchemy.orm import Session
from models import models
from models.models import Role
from schemas.schema import ShowAvocatStat
from utils.hashing import Hash


def getAdminById(id, db: Session):
    result = db.query(models.User).filter(models.User.id == id).first()
    if not result: 
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, Detail=f'Admin with this id = {id} is not available')
    if result.role != Role.admin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, Detail='this user is not an admin')
    return result

def getAvocatById(id, db: Session):
    result = db.query(models.User).filter(models.User.id == id).first()
    if not result: 
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, Detail=f'Admin with this id = {id} is not available')
    if result.role != Role.avocat:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, Detail='this user is not an admin')
    return result

def getAllAvocats(db: Session):
    avocats = db.query(models.User).filter(models.User.role == Role.avocat).all()
    return avocats

# def get_Non_validate_Avos(db: Session):
#    avocats = db.query(models.User).filter(models.User.is_validate == False, models.User.role == Role.avocat).all()
#    return avocats

def get_Non_validate_Avos(db: Session):
    avocats = db.query(models.User, models.Avocat).join(models.Avocat, models.User.id == models.Avocat.userId).filter(models.User.role == Role.avocat, models.Avocat.isValidated == False).all()
    return [ShowAvocatStat( nom=user.nom, prenom=user.prenom, email=user.email, password=user.password, isValidate=avocat.isValidated ) for user, avocat in avocats]

def get_validate_Avos(db: Session):
    avocats = db.query(models.User, models.Avocat).join(models.Avocat, models.User.id == models.Avocat.userId).filter(models.User.role == Role.avocat, models.Avocat.isValidated == True).all() 
    return [ShowAvocatStat( nom=user.nom, prenom=user.prenom, email=user.email, password=user.password, isValidate=avocat.isValidated ) for user, avocat in avocats]

def get_Avocat_by_Id(db: Session, id: int):
    avocat = db.query(models.Avocat).filter(models.Avocat.id == id).first()
    if not avocat : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,Detail =f'Avocat with this email = {id} is not available')
    return avocat


def validate(db: Session, id: str):
    avocat = get_Avocat_by_Id(db,id)
    if avocat.isValidated : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,Detail ="this profile is allredy validated")
    avocat.isValidated = True
    db.commit()
    return {"detail": f"Avocat {id} has been validated"}


def destroyAvo(id, db: Session):
    avocat = get_Avocat_by_Id(db,id)    
    if avocat:
        ID = avocat.userId
        db.delete(avocat)
    user = db.query(models.User).filter(models.User.id == ID).first()
    if user:
        db.delete(user)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, Detail=f'Avocat or User with this id = {id} is not available')
    db.commit()
    return {'avocat deleted Successfuly'}

