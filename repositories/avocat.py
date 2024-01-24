
from sqlalchemy.orm import Session
from models.models import Avocat
from schemas.auth import CreateAvocatSchema
from utils.hashing import Hash
from datetime import datetime


def create(db: Session, avocatSchema: CreateAvocatSchema):
    avocat = Avocat(
        address=avocatSchema['address'],
        wilaya=avocatSchema['wilaya'],
        phoneNumber=avocatSchema['phoneNumber'],
        facebookUrl=avocatSchema['facebookUrl'],
        Wilaya = avocatSchema['Wilaya'],
        description=avocatSchema['description'],
        categories=avocatSchema['categories'],
        userId=avocatSchema['userId'],
        imageUrl=avocatSchema['imageUrl']
    )
    db.add(avocat)
    db.commit()
    db.refresh(avocat)
    return avocat

def get_by_id(db: Session, id: int):
    avocat = db.query(Avocat).filter(Avocat.id == id).first()
    return avocat
