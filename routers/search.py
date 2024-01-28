from fastapi import APIRouter, Depends
from config.db import get_db
from sqlalchemy.orm import Session
from repositories.search import usersearch as usersr, adminsearch as adminsr

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/search")
def search(name:str = '',wilaya:str = '',categories:str = '',page:int = 1,limit:int = 5,db:Session=Depends(get_db)):
    searchResult = usersr(name,wilaya,categories,page,limit,db)
    return searchResult
        
@router.get("/adminsearch")
def adminsearch(name:str = '',wilaya:str = '',categories:str = '',status:str ='accepted',isBlocked:bool = False,page:int = 1,limit:int = 5,db:Session=Depends(get_db)):
    searchResult = adminsr(name,wilaya,categories,status,isBlocked,page,limit,db)
    return searchResult