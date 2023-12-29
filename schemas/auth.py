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
    wilaya:str
    phoneNumber: str
    facebookUrl: str
    description: str
    categories: list[str] = []

class CreateAvocatSchema(BaseModel):
    address: str
    wilaya:str
    phoneNumber: str
    facebookUrl: str
    description: str
    categories: list[str] = []
    userId: int
    imageUrl: str