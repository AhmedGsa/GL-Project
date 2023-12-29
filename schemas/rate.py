from pydantic import BaseModel


class RateSchema(BaseModel):
    avocatId: int
    userId: int
    rate: float
    comment: str