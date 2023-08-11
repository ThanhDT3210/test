from sqlalchemy.sql.schema import ForeignKey
from .database import Base
from sqlalchemy import Column, Integer, String, DateTime
from enum import Enum

class UserRoleEnum(Enum):
    Normal = 1
    BlogManager = 2

class DbUser(Base):
  __tablename__ = 'user'
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String ,nullable=False )
  email = Column(String,nullable=False)
  password = Column(String,nullable=False)
  role = Column(Integer, nullable=False, default=UserRoleEnum.Normal.value, comment="1-Normal, 2-BlogManager")
  create_time = Column(DateTime)
  
