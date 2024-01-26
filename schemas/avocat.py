from datetime import datetime
from pydantic import BaseModel
from typing import List,Optional
from models import enumSTF


class AvocatSchema(BaseModel):
   nom: str
   prenom: str
   email: str
   password: str
   avocat_image :str
   adress :str 
   rating :float
   social :str
   phoneNumber :str
   scheduler:str
   wilaya :Optional[enumSTF.AlgerianWilayas] 
   facebookUrl : str
   description :str
   categories :Optional[enumSTF.AvocateCategoryEnum] = None 

