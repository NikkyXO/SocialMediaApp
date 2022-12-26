from fastapi import APIRouter
from fastapi import FastAPI, Response, Depends, HTTPException, status
from fastapi.params import Body
from app.schema import (
	PostCreateInfo, ResponseSchema, UserResponseModel,
	UserinfoSchema
)
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import *
from app.utils import *




router = APIRouter(
	prefix='/users',
	tags=['User']
)


 
# ADD NEW  USER
@router.post('/add_user', status_code=status.HTTP_201_CREATED, response_model= UserResponseModel)
def create_user(user: UserinfoSchema, db: Session = Depends(get_db)):
	
	hashed_password = hash(user.password)
	user.password = hashed_password

	new_user = User(**user.dict())
	db.add(new_user)
	db.commit()
	db.refresh(new_user)
	return new_user

	

# GET ALL USERS
@router.get('/all', response_model= UserResponseModel)
def get_all_users(db: Session = Depends(get_db)):
	users = db.query(User).all()
	return users



# GET USER BY ID
@router.get('/{id}', response_model= UserResponseModel)
def get_user(id : int, db: Session = Depends(get_db)):
	user = db.query(User).filter(User.id == id).first()

	if not user:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
		detail=f'post with id: {id} doesnt exist')

	return user


# DELETE USER
@router.delete('/{id}')
def delete_user(id : int, db: Session = Depends(get_db)):

	user = db.query(user ).filter(user .id == id).first()

	if not user:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
		detail=f'post with id: {id} doesnt exist')


	db.delete(user)
	db.commit()

	return Response(status_code = status.HTTP_204_NO_CONTENT)
 
