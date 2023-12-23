from sqlalchemy.orm import Session
from models.models import User, Role
from schemas.auth import UserRegisterSchema
from utils.hashing import Hash
from datetime import datetime


def create(db: Session, userSchema: UserRegisterSchema):
    if userSchema.password is None:
        password = None
    else:
        password = Hash.bcrypt(userSchema.password)
    user = User(nom = userSchema.nom, prenom = userSchema.prenom, email = userSchema.email, password = password, role = Role.user, createdAt = datetime.now())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_avocat(db: Session, userSchema: UserRegisterSchema):
    user = User(nom = userSchema.nom, prenom = userSchema.prenom, email = userSchema.email, password = Hash.bcrypt(userSchema.password), role = Role.avocat, createdAt = datetime.now())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_by_email(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    return user