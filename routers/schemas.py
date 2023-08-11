from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
  id : int
  username: str
  email: str
  password: str
  avatar: str
  role: int
  thumbnail: str
  avatar_url_type: str
  thumbnail_url_type: str

class UserDisplay(BaseModel):
  id: int
  username: str
  email: str
  role: int
  create_time: datetime
  class Config():
    from_attributes = True

class UserAuth(BaseModel):
  id: int
  username: str
  email: str

class DeleteResponse(BaseModel):
  msg: str
