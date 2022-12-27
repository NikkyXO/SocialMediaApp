from fastapi import APIRouter
from fastapi import FastAPI, Response, Depends, HTTPException, status, Request, BackgroundTasks
from fastapi.params import Body
from app.schema import PostCreateInfo, ResponseSchema, TokenData, PostOut, Postin, Token
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import *
from app.oauth import get_current_user
from typing import List
from fastapi.security import HTTPBearer
from sqlalchemy import func
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from app.models import *

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(parent_dir, "templates"))

auth_scheme = HTTPBearer()


router = APIRouter(
	prefix='/posts',
	tags=['Post']
)

# @router.get("/", response_class=HTMLResponse)
# async def create_post_html(request: Request, user = Depends(get_current_user)):
#     if not user:
#         return templates.TemplateResponse(
#             "error.html",
#             {
#                 "request": request,
#                 "error": "401 Unauthorized",
#                 "message": "User not logged in.",
#             },
#         )
#     if not user.verified:
#         return templates.TemplateResponse(
#             "error.html",
#             {
#                 "request": request,
#                 "error": "403 Forbidden",
#                 "message": "Verify your account to make posts.",
#             },
#         )
#     return templates.TemplateResponse("make_post.html", {"request": request})






 
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

## COMMENTS AND VOTES
## toggle votes, create comment, delete comment

@router.get("/vote/post/{post_id}")
async def upvote_post(post_id: int, user = Depends(get_current_user), db: Session = Depends(get_db)):

	post_obj = db.query(Post).filter(Post.id == post_id).first()
	# return post_obj
	if not post_obj:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
		detail=f'post with id: {id} doesnt exist')
	try:
		vot_obj = Vote(user_id=user.id, post_id=post_id)
		db.add(vot_obj)
		db.commit()
	except:
		raise HTTPException(status_code=409, detail="Duplicate Voting Not Allowed!")
	# votes = db.query(func.sum(Vote.post_id).label("votes_count"))
	votes = db.query(Post).filter(post_id==post_id).all()

	votes_count = len(votes)
	return f"Voting is successful: Current Vote count for post with id {post_id}  is {votes_count} "

	# will add a background task function later
	
