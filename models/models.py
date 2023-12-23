from config.db import Base
from sqlalchemy import String, Column, Integer, Boolean, DateTime,ForeignKey,Float , JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from models import enumSTF
from sqlalchemy.ext.declarative import declarative_base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    fname = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    created_at = Column(DateTime)
    role =  Column(Enum(enumSTF.RoleEnum), nullable=False)
    is_admin = Column(Boolean)

class Avocat(Base):
    __tablename__ ="avocats"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    fname = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    is_validate = Column(Boolean, default=False)
    createdAt = Column(DateTime)
    role = Column(String(50))   
    __allow_unmapped__ = True
    avocat_image =Column(String(255))
    adress = Column(String(255)) 
    rating = Column(Float)
    social =Column(String(255))
    phoneNumber =Column(String(20))
    scheduler:Column(String(255))
    wilaya = Column(Enum(enumSTF.AlgerianWilayas), nullable=False)
    facebookUrl = Column(String(255))
    description =Column(String(1000))
    categories =  Column(Enum(enumSTF.AvocateCategoryEnum), nullable=False)
    # admin = relationship('Admin', back_populates='lawyers')
    # admin_id = Column(Integer, ForeignKey('admins.id'))    


