from fastapi import APIRouter,Depends,status,HTTPException
from schemas.schema import showAdmin,ShowAvocat,ShowAvocatStat
from typing import List 
from config.db import get_db
from sqlalchemy.orm import Session
from repositories import admin
router =APIRouter(
    prefix ='/admin',
    tags=["Admin"])

@router.get('/{id},',response_model= showAdmin)
async def getById(id :int ,db :Session = Depends(get_db)):
    return admin.getAdminById(id,db)

@router.get('/avocats/ALL',response_model= List[ShowAvocat])
async def getAll(db :Session = Depends(get_db)):
    return admin.getAllAvocats(db);




@router.get('/avocats/NON_Validate',response_model= List[ShowAvocatStat])
async def get_NVAvocat(db :Session = Depends(get_db)):
    return admin.get_Non_validate_Avos(db);



@router.get('/avocats/Validate',response_model= List[ShowAvocatStat])
async def get_VAvocat(db :Session = Depends(get_db)):
    return admin.get_validate_Avos(db);


@router.put("/avocats/{avocat_id}/validate")
async def validate_avocat(avocat_id: int,db :Session = Depends(get_db)):
    return admin.validate(db,avocat_id)
   # Validate the lawyer profile here




@router.delete("/avocats/{avocat_id}")
async def delete_lawyer(avocat_id: int,db :Session = Depends(get_db)):
   return admin.destroyAvo(avocat_id,db)


@router.get('/avocats/{avocat_id}',response_model= ShowAvocat)
async def get_Avocat(avocat_id :str ,db :Session = Depends(get_db)):
    return admin.getAvocatById(avocat_id,db)










