from sqlalchemy.orm.session import Session
from routers.schemas import UserBase, UserDisplay , UserAuth , DeleteResponse
from fastapi import APIRouter, Depends , HTTPException
from db.database import get_db
from db import db_user
from fastapi import APIRouter, Depends, status, UploadFile, File
import random
import string
import shutil
from typing import List
from db.models import DbUser
from db.hashing import Hash
from auth.oauth2 import get_current_user


router = APIRouter(
  prefix='/user',
  tags=['user']
)
user_role = [1 , 2]
@router.post('', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
  if not request.role in user_role:
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
              detail="U can only register role as '1.Normal User or 2.Blog Manager'")
  return db_user.create_user(db, request)

@router.post('/image')
def upload_image(image: UploadFile = File(...)):
  letters = string.ascii_letters
  rand_str = ''.join(random.choice(letters) for i in range(6))
  new = f'_{rand_str}.'
  filename = new.join(image.filename.rsplit('.', 1))
  path = f'images/{filename}'

  with open(path, "w+b") as buffer:
    shutil.copyfileobj(image.file, buffer)
  return {'filename': path}

@router.get('/all' , response_model =List[UserDisplay])
def get_all_users(db: Session = Depends(get_db)):
  return db_user.get_all(db)

@router.get('/get_user_by_name/{name}', response_model = UserDisplay)
def get_user_by_name(name: str, db: Session = Depends(get_db)):
  if db_user.get_user_by_name(db, name) is None:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with name {name} not found")
  return db_user.get_user_by_name(db, name)


@router.get('/get_user_by_id/{id}', response_model = UserDisplay)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
  if db_user.get_user_by_id(db, id) is None:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id {id} not found")
  return db_user.get_user_by_id(db, id)

@router.get('/delete_user/{id}' , response_model= DeleteResponse)
def delete_user(id: int, db: Session = Depends(get_db)):
  user = db_user.delete_user_by_id(db, id)
  if user is None:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id {id} not found")
  return DeleteResponse(msg=f"User with id {id} is deleted")
