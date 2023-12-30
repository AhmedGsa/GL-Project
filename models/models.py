from config.db import Base
from sqlalchemy import ForeignKey, String, Column, Integer, Boolean, DateTime, Enum, JSON
from sqlalchemy.orm import relationship
import enum
from config.const_db import URL_DB
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
class Avocat(Base):
    __tablename__ = "avocat"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(255))
    phoneNumber = Column(String(255))
    facebookUrl = Column(String(255))
    Wilaya = Column(String(255))
    description = Column(String(255))
    status = Column(Enum(AvocatStatus), default="pending")
    isBlocked = Column(Boolean, default=False)
    categories = Column(JSON)
    imageUrl = Column(String(255), nullable=True)
    userId = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="avocat")


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
