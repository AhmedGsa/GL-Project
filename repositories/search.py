from sqlalchemy.orm import Session
from models.models import User, Role,Avocat

class AvocatSearchResult:
    def __init__(self, id,avocatId, nom, prenom, email, createdAt, address, wilaya, phoneNumber, 
                 facebookUrl, description, categories,rate, imageUrl,status,isBlocked):
        self.id = id
        self.avocatId = avocatId
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
        self.rate = rate
        self.imageUrl = imageUrl
        self.status = status
        self.isBlocked = isBlocked

def usersearch(name: str, wilaya: str, categorie: str,page:int,limit:int, db: Session):
    
    searchquery = (
        db.query(User, Avocat)
        .join(Avocat)
        .filter(User.role == Role.avocat)
        .filter(User.id == Avocat.userId)
    )
    #filter only accepted avocats
    searchquery = searchquery.filter(Avocat.status == 'accepted')
    
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

    count = searchquery.count()
    searchresults = searchquery.offset((page-1)*limit).limit(limit).all()

    avocat_search_results = None
    if searchresults:
        
        avocat_search_results = [
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
                imageUrl=avocat_instance.imageUrl,
                status=avocat_instance.status,
                isBlocked=avocat_instance.isBlocked
            )
            for user_instance, avocat_instance in searchresults
        ]

    if(avocat_search_results != None):
        return {
                "result":avocat_search_results,
                "count":count
            }
    else :
        return {"result":"No results found",
                "count":0
                }
    
def adminsearch(name: str, wilaya: str, categorie: str,status:str,isBlocked:bool,page:int,limit:int, db: Session):
    searchquery = (
        db.query(User, Avocat)
        .join(Avocat)
        .filter(User.role == Role.avocat)
        .filter(User.id == Avocat.userId)
    )
    #filter by status and isBlocked
    searchquery = searchquery.filter(Avocat.status == status).filter(Avocat.isBlocked == isBlocked)
    
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
    count = searchquery.count()
    searchresults = searchquery.offset((page-1)*limit).limit(limit).all()

    avocat_search_results = None
    if searchresults:
        
        avocat_search_results = [
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
                imageUrl=avocat_instance.imageUrl,
                status=avocat_instance.status,
                isBlocked=avocat_instance.isBlocked
            )
            for user_instance, avocat_instance in searchresults
        ]
        
    if(avocat_search_results != None):
        return {
                "result":avocat_search_results,
                "count":count
            }
    else :
        return {"result":"No results found",
                "count":0
                }