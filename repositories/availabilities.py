from sqlalchemy.orm import Session
from models.models import Availability

def get_all(db: Session):
    availabilites = db.query(Availability).all()
    print(availabilites)
    return availabilites