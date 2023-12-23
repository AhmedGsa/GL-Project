
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Optional,List
from datetime import datetime
from models import enumSTF
# from enum import Role


#response module 
class AdminSchema(BaseModel):
    name: str
    fname:str
    email: str
    hashed_password :str
    created_at: datetime
    # role : str


class showAdmin(BaseModel):
    name: str
    fnam:str
    email:Optional[str]
    hashed_password :str
    role:Optional[enumSTF.RoleEnum] = None
    class Config():
         orm_mode =True


class ShowAvocatList(BaseModel):
    fname:Optional[str]
    email:Optional[str]
    is_validate:Optional[bool]
    class Config():
        orm_mode =True

class ShowAvocat(BaseModel):
    name :Optional[str]
    prenom:Optional[str]
    email:Optional[str]
    is_validate:Optional[bool]
    class Config():
        orm_mode =True


