from pydantic import BaseModel

class CreateAppointmentSchema(BaseModel):
    phoneNumber: str
    description: str
    avocatId: int
    availabilityId: int
    date: str

class GetAvailableAppointmentTimesSchema(BaseModel):
    avocatId: int
    date: str