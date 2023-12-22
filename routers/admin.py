from fastapi import APIRouter,Depends,status,HTTPException
from schemas.admin import AdminSchema,showAdmin,ShowAvocatList,ShowAvocat
from typing import List 
from config.db import get_db
from sqlalchemy.orm import Session
from repositories import admin
router =APIRouter(
    prefix ='/admin',
    tags=["Admin"])

#CRUD of an admin :
@router.post('/',status_code=status.HTTP_201_CREATED )
async def create_admin(request  :AdminSchema,db :Session = Depends(get_db)):
    return admin.create(request,db)

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT )
async def destroy(id ,db :Session = Depends(get_db)) :
    return admin.destry(id ,db)

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED )
async def update(id :int ,request :AdminSchema ,db :Session = Depends(get_db)):
    return admin.update(id ,request,db )

@router.get('/{id},',response_model= showAdmin)
# async def getById(id :int , nom : str | None = Query(default=None, max_length=50) ,prenom :Annotated[list[str], Query()] = ["foo", "bar"] ,db :Session = Depends(get_db)):
async def getById(id :int ,db :Session = Depends(get_db)):
    return admin.getById(id,db)

#Avocat-Admin interaction :
@router.get('/ALawyers',response_model= List[ShowAvocatList])
async def getAll(db :Session = Depends(get_db)):
    return admin.getAll(db);


@router.get('/lawyers/{avocat_email}',response_model= ShowAvocat)
async def get_Avocat(avocat_email :str ,db :Session = Depends(get_db),):
    return admin.get_Avocat_by_email(db,avocat_email);


@router.get('/NVlawyers',response_model= List[ShowAvocatList])
async def get_NVAvocat(db :Session = Depends(get_db)):
    return admin.get_Non_validate_Avos(db);
@router.get('/Vlawyers',response_model= List[ShowAvocatList])
async def get_VAvocat(db :Session = Depends(get_db)):
    return admin.get_validate_Avos(db);


@router.put("/lawyer/{avocat_email}/validate")
async def validate_lawyer(avocat_email: str,db :Session = Depends(get_db)):
    return admin.validate(db,avocat_email)
   # Validate the lawyer profile here


@router.delete("/lawyer/{avocat_email}")
async def delete_lawyer(avocat_email: str,db :Session = Depends(get_db)):
   return admin.destroyAvo(db,avocat_email)





