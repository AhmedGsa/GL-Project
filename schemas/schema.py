from pydantic import BaseModel
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Optional,List
from datetime import datetime
from models import models
# from enum import Role


#response module 
class AdminSchema(BaseModel):
    nom: str
    prenom:str
    email: str
    password :str
    createdAt: datetime
    # role : str


class showAdmin(BaseModel):
    nom: str
    prenom:str
    email:Optional[str]
    password :str
    role:Optional[models.Role] = None
    class Config():
         orm_mode =True



class ShowAvocat(BaseModel):
    ID:Optional[str]
    nom :Optional[str]
    prenom:Optional[str]
    email:Optional[str]
    phoneNumber:Optional[str]
    Wilaya :Optional[str]
    role:Optional[models.Role] = None
    status:Optional[models.AvocatStatus]
    isBlocked: Optional[bool]
    categories: Optional[List[str]]   
    class Config():
        orm_mode =True
class ShowAvocatStat(BaseModel):
    nom: str
    prenom: str
    email: str
    password: str
    isBlocked: Optional[bool]
    status:Optional[models.AvocatStatus]
    class Config():
        orm_mode =True