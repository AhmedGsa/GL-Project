
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Optional,List
from datetime import datetime
# from enum import Role


#response module 
class AdminSchema(BaseModel):
    nom: str
    prenom:str
    email: str
    hashed_password :str
    created_at: datetime
    # role : str


class showAdmin(BaseModel):
    nom: str
    prenom:str
    hashed_password :str
    # employees: list[ShowAvocatList] = []
    email:Optional[str]
    role:str
    is_Google_user :Optional[bool]
    class Config():
         orm_mode =True


class ShowAvocatList(BaseModel):
    nom:Optional[str]
    prenom:Optional[str]
    email:Optional[str]
    is_validate:Optional[bool]

    class Config():
        orm_mode =True





class ShowAvocat(BaseModel):
    nom:Optional[str]
    prenom:Optional[str]
    email:Optional[str]
    is_validate:Optional[bool]
    class Config():
        orm_mode =True


