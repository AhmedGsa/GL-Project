from datetime import datetime
from pydantic import BaseModel

class LoginSchema(BaseModel):
    email: str
    password: str

class UserRegisterSchema(LoginSchema):
    nom: str
    prenom: str

class AvocatRegisterSchema(UserRegisterSchema):
    address: str
    phoneNumber: str
    facebookUrl: str
    description: str
    categories: list[str] = []

class CreateAvocatSchema(BaseModel):
    address: str
    phoneNumber: str
    facebookUrl: str
    description: str
    categories: list[str] = []
    userId: int
    imageUrl: str