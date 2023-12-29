import datetime
from sqlalchemy.orm import Session
from models.models import Avocat, Comment, Rating, User
from sqlalchemy.sql import func
from schemas.rate import RateSchema
from datetime import datetime

def rateAvocat(rateSchema: RateSchema,db:Session):
    #add the rate and comment to the rating table
    rate = Rating(rate=rateSchema.rate,avocatId=rateSchema.avocatId,userId=rateSchema.userId,createdAt=datetime.now())
    db.add(rate)
    db.commit()
    db.refresh(rate)
    
    if(rateSchema.comment):
        #add the comment to the comment table
        comment = Comment(comment=rateSchema.comment,ratingid=rate.id)
        db.add(comment)
        db.commit()
        db.refresh(comment)
    
    return caluclateAvocatRate(rateSchema.avocatId,db);
    #Update Avocat rating

def caluclateAvocatRate(avocatId:int,db:Session):
    (rounded_avgrating,) = db.query(func.round(func.avg(Rating.rate) * 2) / 2).filter(Rating.avocatId == avocatId).first()
    db.query(Avocat).filter(Avocat.id == avocatId).update({'rate': rounded_avgrating})
    db.commit()
    return rounded_avgrating

def aleadyRated(avocatId:int,userId:int,db:Session):
    if db.query(Rating).filter(Rating.avocatId == avocatId).filter(Rating.userId == userId).first():
        return True
    else:
        return False


class AvocatRatingsAndCommentsResult:
    def __init__(self, userName, rate, comment, createdAt):
        self.userName = userName
        self.rate = rate
        self.comment = comment
        self.createdAt = createdAt

def getAvocatRatingsAndComments(avocatId:int,db:Session):
    results = db.query(Rating,Comment).join(Comment).filter(Rating.avocatId == avocatId).filter(Rating.id == Comment.ratingid).all()
    
    avocat_ratings_and_comments = [
        AvocatRatingsAndCommentsResult(
            userName=result.Rating.user.nom + " " + result.Rating.user.prenom,
            rate=result.Rating.rate,
            comment=result.Comment.comment,
            createdAt=result.Rating.createdAt.strftime("%B %d, %Y"),
        )
        for result in results
    ]
    return avocat_ratings_and_comments