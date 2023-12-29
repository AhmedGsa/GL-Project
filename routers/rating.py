from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
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
    if (not checkavocat or not checkuser):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or Avocat not found")
    #check if the user is rating his self
    if checkuser.id == checkavocat.userId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't rate your self")
    #check if the user already rated this avocat
    if(aleadyRated(rateSchema.avocatId,rateSchema.userId,db)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already rated this avocat")
    #validate the rate
    if(rateSchema.rate < 0 or rateSchema.rate > 5):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Rate must be between 0 and 5")
    newrating = rateAvocat(rateSchema,db)
    return {"rating":newrating}

@router.get("/rate")
def rate(avocatid : int,db:Session=Depends(get_db)):
    #check if  the avocat exist
    checkavocat = avocat.get_by_id(db, avocatid)
    if not checkavocat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avocat not found")
    #return ratings and comments
    return getAvocatRatingsAndComments(avocatid,db)

@router.get("/can-rate")
def canRate(avocatid : int,userid : int,db:Session=Depends(get_db)):
    #check if  the avocat exist
    checkavocat = avocat.get_by_id(db, avocatid)
    checkuser = user.get_by_id(db, userid)
    if (not checkavocat or not checkuser):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or Avocat not found")
    #check if the user already rated this avocat
    if(aleadyRated(avocatid,userid,db) or checkavocat.userId == userid):
        return {"canRate":False}
    else:
        return {"canRate":True}