import enum
from config.db import Base
from sqlalchemy import String, Column, Integer, Boolean, DateTime, Enum,ForeignKey ,Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from enum import Enum

class Role(enum.Enum):
    user = "user"
    admin = "admin"
    avocat = "avocat"

class CategoryEnum(enum.Enum):
    Category1 = "childSex "
    Category2 = "Category2"
    Category3 = "category3"

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255))
    prenom = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    isGoogleUser = Column(Boolean, default=False)
    createdAt = Column(DateTime)
    role = Column(Role, default=Role.user)  
    avocats = relationship("Avocat", back_populates="user")
    admins = relationship("Admin", back_populates="user")


class Avocat(User):
    __tablename__ ="avocats"
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    imgUrl :Column(String(255))
    adress : Column(String(255))
    phoneNumber :Column(String(20))
    facebookUrl = Column(String(255))
    description =Column(String(1000))
    category = Column(ARRAY(Enum(CategoryEnum)))
    user = relationship('User', back_populates='avocats')

# class Category(Base):
#     __tablename__ ="category"
#     id = Column(Integer,primary_key=True,autoincrement=True, index=True)
#     avocatId = Column(Integer,ForeignKey("avocat.id"))
#     category = Column(Enum(CategoryEnum))
#     avocat = relationship('Avocat', back_populates='categories')

class Admin(User):
    __tablename__ = 'admins'
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    nom = Column(String)
    prenom = Column(String)
    email = Column(String)
    password = Column(String)
    user = relationship('User', back_populates='admins')



