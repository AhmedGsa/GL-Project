from config.db import Base
from sqlalchemy import String, Column, Integer, Boolean, DateTime,ForeignKey , JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255))
    prenom = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    isGoogleUser = Column(Boolean, default=False)
    created_at = Column(DateTime)
    role = Column(String(50))

class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255))
    prenom = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    isGoogleUser = Column(Boolean, default=False)
    createdAt = Column(DateTime)
    role = Column(String(50))
    # id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    # lawyers = relationship('Avocat', back_populates='admin')

class Avocat(Base):
    __tablename__ ="avocats"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255))
    prenom = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    is_validate = Column(Boolean, default=False)
    createdAt = Column(DateTime)
    role = Column(String(50))   
    __allow_unmapped__ = True
    avocat_image =Column(String(255))
    adress = Column(String(255))
    phoneNumber =Column(String(20))
    scheduler:Column(String(255))
    facebookUrl = Column(String(255))
    description =Column(String(1000))
    categories = Column(String(20))
    # admin = relationship('Admin', back_populates='lawyers')
    # admin_id = Column(Integer, ForeignKey('admins.id'))    


