
from sqlalchemy.orm import Session
from models.models import Avocat, AvailabilityAvocat
from schemas.auth import CreateAvocatSchema
from utils.hashing import Hash
from datetime import datetime


def create(db: Session, avocatSchema: CreateAvocatSchema):
    avocat = Avocat(
        address=avocatSchema['address'],
        wilaya=avocatSchema['Wilaya'],
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
    for availabilityId in avocatSchema['availabilityIds']:
        db.add(AvailabilityAvocat(availabilityId=availabilityId, avocatId=avocat.id))
    db.commit()
    db.refresh(avocat)
    return avocat

def update(db: Session, userId: int, avocatSchema: CreateAvocatSchema):
    avocat = get_by_user_id(db, userId)
    avocat.address = avocatSchema['address']
    avocat.wilaya = avocatSchema['Wilaya']
    avocat.phoneNumber = avocatSchema['phoneNumber']
    avocat.facebookUrl = avocatSchema['facebookUrl']
    avocat.description = avocatSchema['description']
    avocat.categories = avocatSchema['categories']
    avocat.longitude = avocatSchema['longitude']
    avocat.latitude = avocatSchema['latitude']
    avocat.imageUrl = avocatSchema['imageUrl'] if avocatSchema['imageUrl'] else avocat.imageUrl
    avocat.workDays = avocatSchema['workDays']
    db.commit()
    db.refresh(avocat)
    db.query(AvailabilityAvocat).filter(AvailabilityAvocat.avocatId == avocat.id).delete()
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

def get_all_info_by_user_id(db: Session, userId: int):
    avocat = db.query(Avocat).filter(Avocat.userId == userId).first()
    avocat.availabilityIds = [availability.availabilityId for availability in db.query(AvailabilityAvocat).filter(AvailabilityAvocat.avocatId == avocat.id).all()]
    return avocat
