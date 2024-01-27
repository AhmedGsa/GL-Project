from pydantic import BaseModel

class ChangePassword(BaseModel):
    oldPassword: str
    newPassword: str