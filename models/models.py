from config.db import Base
from sqlalchemy import ForeignKey, String, Column, Integer, Boolean, DateTime,Float, Enum, JSON
from sqlalchemy.orm import relationship
import enum

class Role(enum.Enum):
    user = "user"
    admin = "admin"
    avocat = "avocat"

class AvocatStatus(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255))
    prenom = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255), nullable=True)
    isGoogleUser = Column(Boolean, default=False)
    createdAt = Column(DateTime)
    role = Column(Enum(Role), default="user")
    avocat = relationship("Avocat", back_populates="user")
    rating = relationship("Rating", back_populates="user")

class Avocat(Base):
    __tablename__ = "avocat"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(255))
    wilaya = Column(String(50))
    phoneNumber = Column(String(255))
    facebookUrl = Column(String(255))
    description = Column(String(255))
    status = Column(Enum(AvocatStatus), default="pending")
    isBlocked = Column(Boolean, default=False)
    categories = Column(JSON)
    rate = Column(Float, default=0)
    imageUrl = Column(String(255), nullable=True)
    userId = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="avocat")
    rating = relationship("Rating", back_populates="avocat")
    
class Rating(Base):
    __tablename__ = "rating"
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("user.id"))
    avocatId = Column(Integer, ForeignKey("avocat.id"))
    rate = Column(Float)
    createdAt = Column(DateTime)
    avocat = relationship("Avocat", back_populates="rating")
    user = relationship("User", back_populates="rating")
    comment = relationship("Comment", back_populates="rating")
    
class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True, index=True)
    ratingid = Column(Integer, ForeignKey("rating.id"))
    comment = Column(String(255))
    rating = relationship("Rating", back_populates="comment")
