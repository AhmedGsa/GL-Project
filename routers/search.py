from fastapi import APIRouter, Depends, Form
from config.db import get_db
from sqlalchemy.orm import Session
from repositories import search as sr
from typing import Annotated,Optional

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/search")
def search(name:str = '',wilaya:str = '',categories:str = '',page:int = 1,limit:int = 25,db:Session=Depends(get_db)):
    searchResult = sr.search(name,wilaya,categories,page,limit,db)
    if(searchResult != None):
        return {"result":searchResult}
    else :
        return {"result":"No results found"}