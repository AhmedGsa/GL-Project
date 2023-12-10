
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import Admin
from typing import Optional,List
from datetime import datetime
# from enum import Role
from datetime import datetime
from models import Role ,CategoryEnum

class AvocatBase(BaseModel):
   nom: str
   prenom: str
   email: str
   password: str
   isGoogleUser: bool
   createdAt: datetime
   role: Role
   imgUrl: str
   adress: str
   phoneNumber: str
   facebookUrl: str
   description: str
   category: List[CategoryEnum]

#response module 
class showAdmin(BaseModel):
    nom: Optional[str]
    prenom: Optional[str]
    email:Optional[str]
    role:Optional[Role]
    is_Google_user :Optional[bool]
    class Config():
         orm_mode =True
