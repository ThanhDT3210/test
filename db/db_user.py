from fastapi import HTTPException, status
from .models import DbUser
from routers.schemas import UserBase , UserDisplay
from sqlalchemy.orm.session import Session
from .hashing import Hash
import datetime
from enum import Enum

image_url_types = ['absolute', 'relative']

user_role = [1 , 2]

def is_email_available(db: Session, email: str) -> bool:
    user = db.query(DbUser).filter(DbUser.email == email).first()
    return not bool(user)

def create_user(db: Session, request: UserBase):
  if not is_email_available(db, request.email):
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Email {request.email} is already taken')
  new_user = DbUser(
    username = request.username,
    email = request.email,
    password = Hash.bcrypt(request.password),
    role = request.role,
    create_time = datetime.datetime.now()
  )
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

def get_all(db: Session):
  return db.query(DbUser).all()

def get_user_by_name(db: Session, username: str):
  user = db.query(DbUser).filter(DbUser.username == username).first()
  if not user:
    return None
  return user

def get_user_by_id(db: Session , id: int):
  user = db.query(DbUser).filter(DbUser.id == id).first()
  if not user:
    return None
  return user

def delete_user_by_id(db: Session, id: int):
  user = db.query(DbUser).filter(DbUser.id == id).first()
  if not user:
    return None
  db.delete(user)
  db.commit()
  return user
