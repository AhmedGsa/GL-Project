from datetime import datetime
from pydantic import BaseModel

class LoginSchema(BaseModel):
    email: str
    password: str

class UserRegisterSchema(LoginSchema):
    nom: str
    prenom: str