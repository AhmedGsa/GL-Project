
from enum import Enum


from sqlalchemy import String, Column, Integer, Boolean, DateTime, Enum,ForeignKey ,Enum



class RoleEnum(Enum):
  admin = 1
  user = 2
  avocat = 3

class CategoryEnum(Enum):
    Category1 = "Category1 "
    Category2 = "Category2"
    Category3 = "category3"

