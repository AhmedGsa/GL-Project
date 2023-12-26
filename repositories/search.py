from sqlalchemy.orm import Session
from models.models import User, Role,Avocat
from sqlalchemy import func

class AvocatSearchResult:
    def __init__(self, id, nom, prenom, email, createdAt, address, wilaya, phoneNumber, 
                 facebookUrl, description, categories, imageUrl):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.createdAt = createdAt
        self.address = address
        self.wilaya = wilaya
        self.phoneNumber = phoneNumber
        self.facebookUrl = facebookUrl
        self.description = description
        self.categories = categories
        self.imageUrl = imageUrl

def search(name: str, wilaya: str, categorie: str,page:int,limit:int, db: Session):
    
    searchquery = (
        db.query(User, Avocat)
        .join(Avocat)
        .filter(User.role == Role.avocat)
        .filter(User.id == Avocat.userId)
    )
    #filter with name
    if len(name) > 0:
        for element in name.split(' '):
            searchquery = searchquery.filter(User.nom.like(f"%{element}%")|User.prenom.like(f"%{element}%"))
        
    #filter with wilaya if wilaya > 0
    if len(wilaya) > 0:
        searchquery = searchquery.filter(Avocat.wilaya == wilaya)
        
    #filter with Category if they give a list of categorie from the frontend
    if len(categorie) > 0:
        searchquery = searchquery.filter(Avocat.categories.contains(categorie))

    searchresults = searchquery.offset((page-1)*limit).limit(limit).all()

    if searchresults:
        
        avocat_search_results = [
            AvocatSearchResult(
                id=user_instance.id,
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
                imageUrl=avocat_instance.imageUrl
            )
            for user_instance, avocat_instance in searchresults
        ]
        return avocat_search_results
    else:
        return None