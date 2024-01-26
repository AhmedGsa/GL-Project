from datetime import datetime
from pydantic import BaseModel

class LoginSchema(BaseModel):
    email: str
    password: str

class UserRegisterSchema(BaseModel):
    email: str
    password: str | None = None
    nom: str
    prenom: str

class AvocatRegisterSchema(UserRegisterSchema):
    address: str
    phoneNumber: str
    facebookUrl: str
    Wilaya :str
    description: str
    longitude: float
    latitude: float
    categories: list[str] = []
    workDays: list[str] = []
    availabilityIds: list[str] = []

class CreateAvocatSchema(BaseModel):
    address: str
    phoneNumber: str
    facebookUrl: str
    Wilaya :str
    description: str
    longitude: float
    latitude: float
    categories: list[str] = []
    workDays: list[str] = []
    availabilityIds: list[str] = []
    userId: int
    imageUrl: str