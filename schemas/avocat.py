from datetime import datetime
from pydantic import BaseModel
from typing import List,Optional


class AvocatSchema(BaseModel):
   nom: str
   prenom: str
   email: str
   hashed_password: str
   createdAt: datetime
   avocat_image: str
   adress: str
   role :str
   phoneNumber: str
   facebookUrl: str
   description: str


