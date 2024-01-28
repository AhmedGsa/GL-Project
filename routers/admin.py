from fastapi import APIRouter,Depends,status,HTTPException
from schemas.schema import showAdmin,ShowAvocat,ShowAvocatStat
from typing import List 
from config.db import get_db
from sqlalchemy.orm import Session
from repositories import admin

router =APIRouter(
    prefix ='/admin',
    tags=["Admin"])
{
    "data":[...],
    "pagenation":{
        "next":"link to the next page",
        "previous":"link to the privious page",
    },
    "count":"total number of items",
    "total":"total number of items"
}
@router.get('/{id}',response_model= showAdmin)
async def getById(id :int ,db :Session = Depends(get_db)):
    return admin.getAdminById(id,db)

# @router.get('/avocats/{avocat_id}',response_model= ShowAvocat)
# async def get_Avocat(avocat_id :str ,db :Session = Depends(get_db)):
#     return admin.get_Avocat_by_Avocat_Id(db,avocat_id)

@router.get('/avocats/ALL')
async def getAll(page_num:int =1,page_size:int =10,db :Session = Depends(get_db)):
    return admin.getAllAvocats(page_num,page_size,db);


@router.get('/avocats/Validate',response_model= List[ShowAvocat])
async def get_VAvocat(db :Session = Depends(get_db)):
    return admin.get_validate_Avos(db);


@router.get('/avocats/NON_Validate',response_model= List[ShowAvocat])
async def get_NVAvocat(db :Session = Depends(get_db)):
    return admin.get_Non_validate_Avos(db);



@router.put("/avocats/{avocat_id}/validate")
async def validate_avocat(avocat_id: int,db :Session = Depends(get_db)):
    return admin.accepte(db,avocat_id)


@router.put("/avocats/{avocat_id}/Invalidate")
async def Invalidate_avocat(avocat_id: int,db :Session = Depends(get_db)):
    return admin.Invalide(db,avocat_id)

@router.put("/avocats/{avocat_id}/Blocked")
async def Block_avocat(avocat_id: int,db :Session = Depends(get_db)):
    return admin.block(db,avocat_id)

@router.put("/avocats/{avocat_id}/UnBlocked")
async def UnBlock_avocat(avocat_id: int,db :Session = Depends(get_db)):
    return admin.Unblock(db,avocat_id)


@router.delete("/avocats/{avocat_id}")
async def delete_lawyer(avocat_id: int,db :Session = Depends(get_db)):
   return admin.destroyAvo(avocat_id,db)

@router.delete("/users/{user_email}")
async def delete_user(user_email: str,db :Session = Depends(get_db)):
   return admin.destroyUser(user_email,db)













