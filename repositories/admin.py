
from fastapi import status ,HTTPException
from sqlalchemy.orm import Session
from models import models
from models.models import Role,AvocatStatus
from schemas.schema import ShowAvocat
from utils.hashing import Hash



def format_id(id: int) -> str:
   return f"ID#{id}"


def getAdminById(id, db: Session):
    result = db.query(models.User).filter(models.User.id == id).first()
    if not result: 
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Admin with this id = {id} is not available')
    if result.role != Role.admin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='this user is not an admin')
    return result


def get_Avocat_By_User_Id(id, db: Session):
    result = db.query(models.User).filter(models.User.id == id).first()
    if not result: 
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Admin with this id = {id} is not available')
    if result.role != Role.avocat:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='this user is not an admin')
    return result


def get_Avocat_by_Avocat_Id(db: Session, id: int):
    avocat = db.query(models.Avocat).filter(models.Avocat.id == id).first()
    if not avocat : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail =f'Avocat with this email = {id} is not available')
    return avocat


def getAllAvocats(page_num:int,page_size:int ,db: Session):
    start = (page_num - 1) * page_size
    end = start + page_size
       
    avocats = db.query(models.Avocat).join(models.User).all()
    total_avocats = len(avocats)
    if start >= total_avocats:
        return {"message": "Page not available"}
  
    if end > total_avocats:
        end = total_avocats

    sliced_avocats = avocats[start:end]
    response ={
       "data": [ShowAvocat(ID =format_id(avocat.user.id), nom=avocat.user.nom, prenom=avocat.user.prenom, email=avocat.user.email, role=avocat.user.role, phoneNumber=avocat.phoneNumber, Wilaya=avocat.Wilaya, status=avocat.status, isBlocked=avocat.isBlocked, categories=avocat.categories) for avocat in sliced_avocats],
       "total": total_avocats,
        "count":page_size,
        "pagination":{
            "previous": page_num - 1 if page_num > 1 else None,
            "next": page_num + 1 if end < total_avocats else None
        }
    }

    return response




def get_Non_validate_Avos(db: Session):
   avocats = db.query(models.User, models.Avocat).join(models.Avocat, models.User.id == models.Avocat.userId).filter(models.User.role == Role.avocat, models.Avocat.status == AvocatStatus.pending).all()
   return [ShowAvocat(ID =format_id(avocat.user.id) ,nom=user.nom, prenom=user.prenom, email=user.email,role=avocat.user.role, phoneNumber=avocat.phoneNumber, Wilaya=avocat.Wilaya, status=avocat.status, isBlocked=avocat.isBlocked, categories=avocat.categories) for user, avocat in avocats]

def get_validate_Avos(db: Session):
    avocats = db.query(models.User, models.Avocat).join(models.Avocat, models.User.id == models.Avocat.userId).filter(models.User.role == Role.avocat, models.Avocat.status == AvocatStatus.accepted).all() 
    return [ShowAvocat(ID =format_id(avocat.user.id),nom=user.nom, prenom=user.prenom, email=user.email,role=avocat.user.role, phoneNumber=avocat.phoneNumber, Wilaya=avocat.Wilaya, status=avocat.status, isBlocked=avocat.isBlocked, categories=avocat.categories) for user, avocat in avocats]


def accepte(db: Session, id: str):
    avocat = get_Avocat_by_Avocat_Id(db,id)
    if avocat.isBlocked:
       avocat.isBlocked = False
       models.Avocat.status == AvocatStatus.pending
       avocat.status = AvocatStatus.pending
    elif avocat.status == AvocatStatus.accepted:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="this avocat is already accepted")
    elif avocat.status == AvocatStatus.pending and not avocat.isBlocked:
       avocat.status = AvocatStatus.accepted
    db.commit()
    return {"detail": f"Avocat {id} has been accepted"}

def Invalide(db: Session, id: str):
    avocat = get_Avocat_by_Avocat_Id(db,id)
    if avocat.isBlocked:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="this avocat is Blocked")
    elif avocat.status == AvocatStatus.pending:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="this avocat is already in pending")
    elif avocat.status == AvocatStatus.accepted and not avocat.isBlocked:
       avocat.status = AvocatStatus.pending
    db.commit()
    return {"detail": f"Avocat {id} has been pended"}

def block(db: Session, id: str):
    avocat = get_Avocat_by_Avocat_Id(db,id)
    if avocat.isBlocked:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="this avocat is already Blocked")
    avocat.isBlocked = True
    avocat.status = AvocatStatus.pending
    db.commit()
    return {"detail": f"Avocat {id} has been Blocked"}

def Unblock(db: Session, id: str):
    avocat = get_Avocat_by_Avocat_Id(db,id)
    if not avocat.isBlocked:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="this avocat is already UnBlocked")
    avocat.isBlocked = False
    avocat.status = AvocatStatus.pending
    db.commit()
    return {"detail": f"Avocat {id} has been UnBlocked"}


def destroyAvo(id, db: Session):
    avocat = get_Avocat_by_Avocat_Id(db,id)    
    if avocat:
        ID = avocat.userId
        db.delete(avocat)
    user = db.query(models.User).filter(models.User.id == ID).first()
    if user:
        db.delete(user)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Avocat or User with this id = {id} is not available')
    db.commit()
    return {'avocat deleted Successfuly'}


def destroyUser(email, db: Session):

    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        db.delete(user)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Avocat or User with this id = {id} is not available')
    db.commit()
    return {'avocat deleted Successfuly'}