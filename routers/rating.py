from fastapi import APIRouter, Depends, HTTPException, Request,status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from config.db import get_db
from repositories.rating import aleadyRated, getTopRated, getUserRatings, rateAvocat,getAvocatRatingsAndComments
from schemas.rate import RateSchema
from repositories import avocat,user



router = APIRouter(prefix="/rating", tags=["Rating"])

bearer_scheme = HTTPBearer()

@router.post("/rate")
def rate(request:Request,rateSchema: RateSchema, token: str = Depends(bearer_scheme),db:Session=Depends(get_db)):
    #check if the user and the avocat exist
    checkavocat = avocat.get_by_id(db, rateSchema.avocatId)
    checkuser = user.get_by_id(db, request.state.user["id"])
    if (not checkavocat or not checkuser):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or Avocat not found")
    #check if the user is rating his self
    if checkuser.id == checkavocat.userId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't rate your self")
    #check if the user already rated this avocat
    if(aleadyRated(rateSchema.avocatId,request.state.user["id"],db)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already rated this avocat")
    #validate the rate
    if(rateSchema.rate < 0 or rateSchema.rate > 5):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Rate must be between 0 and 5")
    newrating = rateAvocat(rateSchema,request.state.user["id"],db)
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
    if(aleadyRated(avocatid,userid,db)):
        return {"canRate":False}
    else:
        return {"canRate":True}
    
@router.get("/top-rated")
def topRated(limit:int,db:Session=Depends(get_db)):
    topRatedAvocats = getTopRated(limit,db)
    return topRatedAvocats

@router.get("/user-ratings")
def userRatings(request:Request, token: str = Depends(bearer_scheme),db:Session=Depends(get_db)):
    return getUserRatings(request.state.user["id"],db)