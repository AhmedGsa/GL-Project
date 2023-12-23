from config.db import Base
from sqlalchemy import String, Column, Integer, Boolean, DateTime, Enum
import enum

class Role(enum.Enum):
    user = "user"
    admin = "admin"
    avocat = "avocat"

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
    role = Column(Enum(Role), default="user")
