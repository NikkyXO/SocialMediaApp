from fastapi import APIRouter
from fastapi import FastAPI, Response, Depends, HTTPException, status
from fastapi.params import Body
from app.schema import PostCreateInfo, ResponseSchema, TokenData, PostOut, Postin, Token
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import *
from app.oauth import get_current_user
from typing import List
from fastapi.security import HTTPBearer
from sqlalchemy import func


auth_scheme = HTTPBearer()


router = APIRouter(
	prefix='/posts',
	tags=['Post']
)


 
# ADD NEW  POSTS
@router.post('/add_post', status_code=status.HTTP_201_CREATED, response_model= ResponseSchema)
def create_post(post: PostCreateInfo,  db: Session = Depends(get_db),
	current_user: TokenData =  Depends(get_current_user)): # 
	 

	post_obj = Post(owner_id=current_user.id, **post.dict())
	db.add(post_obj)
	db.commit()
	db.refresh(post_obj)

	return post_obj
	# except BaseException:
	# 	return {"error": "invalid details"}
	


# GET LATEST POST
@router.get('/latest', response_model= List[ResponseSchema])
def get_latest_post(db: Session = Depends(get_db)):
	posts = db.query(Post).order_by(Post.id.desc()).first()

	return posts
	

# GET ALL POSTS
@router.get('/all', response_model= ResponseSchema)
def get_all_post(db: Session = Depends(get_db)):
	posts = db.query(Post).all()
	return posts



# GET POST BY ID
@router.get('/{id}', response_model= PostOut)
def get_post(id : int, db: Session = Depends(get_db)):
	post_obj = db.query(Post, func.count(Vote.post_id).label('votes')).join(
		Vote, Vote.post_id == Post.id, isouter=True).group_by(Post.id).filter(Post.id == id).first()



	if not post_obj:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
		detail=f'post with id: {id} doesnt exist')

	return post_obj


# DELETE POSTS
@router.delete('/{id}')
def delete_post(id : int, db: Session = Depends(get_db), 
	current_user :  int =  Depends(get_current_user)):

	post_obj = db.query(Post).filter(Post.id == id).first()

	if not post_obj:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
		detail=f'post with id: {id} doesnt exist')

	if post_obj.owner_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
							detail="Not authorized to perform requested action")

	db.delete(post_obj)
	db.commit()

	return Response(status_code = status.HTTP_204_NO_CONTENT)


# UPDATE POSTS
@router.put('/{id}', response_model= Postin)
def update_post(id : int, updated_post: PostCreateInfo, db: Session = Depends(get_db), 
	current_user :  int =  Depends(get_current_user)):

	post_obj = db.query(Post).filter(Post.id == id).first()

	if not post_obj:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
		detail=f'post with id: {id} doesnt exist')

	if post_obj.owner_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
							detail="Not authorized to perform requested action")

	# post_obj(updated_post.dict())

	post_obj.title = post.title
	post_obj.content = post.content
	post_obj.published = post.published
	

	# saving 
	db.add(post_obj)
	db.commit()
	db.refresh(post_obj)
	return post_obj