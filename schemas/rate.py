from pydantic import BaseModel


class RateSchema(BaseModel):
    avocatId: int
    rate: float
    comment: str