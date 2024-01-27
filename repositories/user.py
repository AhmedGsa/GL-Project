from sqlalchemy.orm import Session
from models.models import User,Role
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

def get_by_id(db: Session, id: int):
    user = db.query(User).filter(User.id == id).first()
    return user

def update(db: Session, userId: int, userSchema: UserRegisterSchema):
    user = get_by_id(db, userId)
    user.nom = userSchema.nom
    user.prenom = userSchema.prenom
    user.email = userSchema.email
    db.commit()
    db.refresh(user)
    return user

def update_password(db: Session, userId: int, newPassword: str):
    user = get_by_id(db, userId)
    user.password = Hash.bcrypt(newPassword)
    db.commit()
    db.refresh(user)
    return user
