from pydantic import BaseModel

class UserRegisterSchema(BaseModel):
    nom: str
    prenom: str
    email: str
    password: str