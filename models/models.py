from config.db import Base
from sqlalchemy import String, Column, Integer, Boolean, DateTime, Enum
import enum

class Role(enum.Enum):
    user = "user"
    admin = "admin"
    avocat = "avocat"

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255))
    prenom = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    isGoogleUser = Column(Boolean, default=False)
    createdAt = Column(DateTime)
    role = Column(Enum(Role), default="user")
