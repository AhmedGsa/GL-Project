from fastapi import APIRouter,Depends,status,HTTPException
from schemas.avocat import AvocatSchema
from typing import List 
from config.db import get_db
from sqlalchemy.orm import Session
from repositories import avocat

router =APIRouter(
    prefix ='/avocat',
    tags=["Avocat"])


#create an avocat :
@router.post('/',status_code=status.HTTP_201_CREATED )
async def create_avocat(request  :AvocatSchema,db :Session = Depends(get_db)):
    return avocat.Avocatcreate(request,db)

