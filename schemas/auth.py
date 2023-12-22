from datetime import datetime
from pydantic import BaseModel
from typing import List,Optional


class LoginSchema(BaseModel):
    email: str
    password: str

class UserRegisterSchema(LoginSchema):
    nom: str
    prenom: str
    email:str

# class AvocatRegisterSchema(UserRegisterSchema):
#     facebookURL : str
#     categories : List[str]

class AvocatRegisterSchema(BaseModel):
   nom: str
   prenom: str
   email: str
   hashed_password: str
   isGoogleUser: bool
   createdAt: datetime
   avocat_image: str
   adress: str
   role :str
   phoneNumber: str
   facebookUrl: str
   description: str


