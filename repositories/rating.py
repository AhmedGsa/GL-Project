import datetime
from sqlalchemy import desc
from sqlalchemy.orm import Session
from models.models import Avocat, Comment, Rating, User
from sqlalchemy.sql import func
from repositories.search import AvocatSearchResult
from schemas.rate import RateSchema
from datetime import datetime

def rateAvocat(rateSchema: RateSchema,userId:int,db:Session):
    #add the rate and comment to the rating table
    rate = Rating(rate=rateSchema.rate,userId = userId,avocatId=rateSchema.avocatId,createdAt=datetime.now())
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
    (roundedavgrating,) = db.query(func.round(func.avg(Rating.rate) * 2) / 2).filter(Rating.avocatId == avocatId).first()
    db.query(Avocat).filter(Avocat.id == avocatId).update({'rate': roundedavgrating})
    db.commit()
    return roundedavgrating

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


def getTopRated(limit:int , db:Session):
    mostRated = (
        db.query(User, Avocat)
        .join(Avocat)
    )
    #filter by status and isBlocked
    mostRated = mostRated.filter(Avocat.status == "accepted").filter(Avocat.isBlocked == False)
    
    #order by rating and limit
    mostRated = mostRated.order_by(desc(Avocat.rate)).limit(limit).all()

    if mostRated:
        
        avocat_Most_Rated = [
            AvocatSearchResult(
                id=user_instance.id,
                avocatId = avocat_instance.id,
                nom=user_instance.nom,
                prenom=user_instance.prenom,
                email=user_instance.email,
                createdAt=user_instance.createdAt,
                address=avocat_instance.address,
                wilaya=avocat_instance.wilaya,
                phoneNumber=avocat_instance.phoneNumber,
                facebookUrl=avocat_instance.facebookUrl,
                description=avocat_instance.description,
                categories=avocat_instance.categories,
                rate=avocat_instance.rate,
                imageUrl=avocat_instance.imageUrl
            )
            for user_instance, avocat_instance in mostRated
        ]
        return avocat_Most_Rated
    else:
        return None