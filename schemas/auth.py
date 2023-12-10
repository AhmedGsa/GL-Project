from datetime import datetime
from models import Role ,CategoryEnum
from pydantic import BaseModel
from typing import List

class LoginSchema(BaseModel):
    email: str
    password: str

class UserRegisterSchema(LoginSchema):
    nom: str
    prenom: str

class AvocatRegisterSchema(UserRegisterSchema):
    facebookURL : str
    categories : List[str]

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
