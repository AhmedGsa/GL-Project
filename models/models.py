from config.db import Base
from sqlalchemy import ForeignKey, String, Column, Integer, Boolean, DateTime, Float, Enum, JSON, Date, Text
from sqlalchemy.orm import relationship
import enum
from config.const_db import URL_DB
class Role(enum.Enum):
    user = "user"
    admin = "admin"
    avocat = "avocat"

class Days(enum.Enum):
    lundi = "lundi"
    mardi = "mardi"
    mercredi = "mercredi"
    jeudi = "jeudi"
    vendredi = "vendredi"
    samedi = "samedi"
    dimanche = "dimanche"

class AvocatStatus(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"

class AppointmentStatus(enum.Enum):
    pending = "pending"
    done = "done"
    canceled = "canceled"

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
    appointments = relationship("Appointment", back_populates="user")

class Avocat(Base):
    __tablename__ = "avocat"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(255))
    wilaya = Column(String(50))
    phoneNumber = Column(String(255))
    facebookUrl = Column(String(255))
    description = Column(Text)
    status = Column(Enum(AvocatStatus), default="pending")
    isBlocked = Column(Boolean, default=False)
    categories = Column(JSON)
    workDays = Column(JSON)
    rate = Column(Float, default=0)
    imageUrl = Column(String(255), nullable=True)
    longitude = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    userId = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="avocat")
    rating = relationship("Rating", back_populates="avocat")
    availabilities = relationship("AvailabilityAvocat", back_populates="avocat")
    appointments = relationship("Appointment", back_populates="avocat")
    
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


class Availability(Base):
    __tablename__ = "availability"
    id = Column(Integer, primary_key=True, index=True)
    start = Column(String(255))
    end = Column(String(255))
    avocats = relationship("AvailabilityAvocat", back_populates="availability")
    appointments = relationship("Appointment", back_populates="availability")

class AvailabilityAvocat(Base):
    __tablename__ = "availability_avocat"
    avocatId = Column(Integer, ForeignKey("avocat.id"), primary_key=True)
    avocat = relationship("Avocat", back_populates="availabilities")
    availabilityId = Column(Integer, ForeignKey("availability.id"), primary_key=True)
    availability = relationship("Availability", back_populates="avocats")

class Appointment(Base):
    __tablename__ = "appointment"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    status = Column(Enum(AppointmentStatus), default="pending")
    phoneNumber = Column(String(255))
    description = Column(String(255))
    avocatId = Column(Integer, ForeignKey("avocat.id"))
    avocat = relationship("Avocat", back_populates="appointments")
    userId = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="appointments")
    availabilityId = Column(Integer, ForeignKey("availability.id"))
    availability = relationship("Availability", back_populates="appointments")


# import json
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# # Load the data from the JSON file
# with open('Scraped_Data.json') as f:
#    data = json.load(f)

# # Create a new engine and session
# engine = create_engine(URL_DB)
# Session = sessionmaker(bind=engine)
# session = Session()

# # Loop through each record in the data
# for record in data:
#    # Create a new User and Avocat object
#    user = User(
#        nom=record["name"],
#        prenom=record["fname"],
#        email=record["email"],
#        password=None,
#        isGoogleUser=False,
#        createdAt=DateTime.utcnow(),
#        role=Role.avocat
#    )
#    avocat = Avocat(
#        address=record["address"],
#        phoneNumber=record["phone"],
#        facebookUrl=None,
#        Wilaya=record["wilaya"][0] if record["wilaya"] else None,
#        description=record["description"],
#        status=AvocatStatus.pending,
#        isBlocked=False,
#        categories=record["categories"],
#        imageUrl=record["avocat_image"],
#        userId=user.id
#    )
   
#    # Add the objects to the session
#    session.add(user)
#    session.add(avocat)

# # Commit the transaction
# session.commit()
