from sqlalchemy.orm import Session
from models.models import User, Role,Avocat,Category,CategoryEnum
from schemas.auth import AvocatRegisterSchema
from utils.hashing import Hash
from datetime import datetime


def create(db: Session, avocatSchema: AvocatRegisterSchema):
    user = User(nom = avocatSchema.nom, prenom = avocatSchema.prenom, email = avocatSchema.email, password = Hash.bcrypt(avocatSchema.password), role = Role.user, createdAt = datetime.now())
    db.add(user)
    db.commit()
    db.refresh(user)
    avocat = Avocat(userid = user.id,facebookurl = avocatSchema.facebookURL)
    db.add(avocat)
    db.commit()
    db.refresh(avocat)

    for cat in avocatSchema.categories:
        category = Category(avocatId = avocat.id,category =CategoryEnum(cat))
        db.add(category)
        db.commit()
        db.refresh(category)

    return user

def get_by_email(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    return user