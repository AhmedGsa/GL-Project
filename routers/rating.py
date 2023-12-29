from fastapi import APIRouter, Depends, HTTPException,status
from mysqlx import Session
from config.db import get_db
from repositories.rating import aleadyRated, rateAvocat,getAvocatRatingsAndComments
from schemas.rate import RateSchema
from repositories import avocat,user


router = APIRouter(prefix="/rating", tags=["Rating"])


@router.post("/rate")
def rate(rateSchema: RateSchema,db:Session=Depends(get_db)):
    #check if the user and the avocat exist
    checkavocat = avocat.get_by_id(db, rateSchema.avocatId)
    checkuser = user.get_by_id(db, rateSchema.userId)
    if not avocat or not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or Avocat not found")
    if(aleadyRated(rateSchema.avocatId,rateSchema.userId,db)):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already rated this avocat")
    
    return rateAvocat(rateSchema,db)

@router.get("/rate")
def rate(avocatid : int,db:Session=Depends(get_db)):
    #check if  the avocat exist
    checkavocat = avocat.get_by_id(db, avocatid)
    if not avocat:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avocat not found")
    return getAvocatRatingsAndComments(avocatid,db)
