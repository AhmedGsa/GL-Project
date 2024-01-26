from sqlalchemy.orm import Session
from models.models import Avocat, AvailabilityAvocat
from schemas.auth import CreateAvocatSchema
from utils.hashing import Hash
from datetime import datetime


def create(db: Session, avocatSchema: CreateAvocatSchema):
    avocat = Avocat(
        address=avocatSchema['address'],
        wilaya=avocatSchema['wilaya'],
        phoneNumber=avocatSchema['phoneNumber'],
        facebookUrl=avocatSchema['facebookUrl'],
        description=avocatSchema['description'],
        categories=avocatSchema['categories'],
        longitude=avocatSchema['longitude'],
        latitude=avocatSchema['latitude'],
        userId=avocatSchema['userId'],
        imageUrl=avocatSchema['imageUrl'],
        workDays=avocatSchema['workDays'],
    )
    db.add(avocat)
    db.commit()
    db.refresh(avocat)
    print(avocatSchema['availabilityIds'])
    for availabilityId in avocatSchema['availabilityIds']:
        db.add(AvailabilityAvocat(availabilityId=availabilityId, avocatId=avocat.id))
    db.commit()
    db.refresh(avocat)
    return avocat

def get_by_id(db: Session, id: int):
    avocat = db.query(Avocat).filter(Avocat.id == id).first()
    return avocat

def get_by_user_id(db: Session, userId: int):
    avocat = db.query(Avocat).filter(Avocat.userId == userId).first()
    return avocat