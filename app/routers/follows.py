from app.schema import *
from fastapi import FastAPI, Response, Depends, HTTPException, status, APIRouter
from app.database import get_db
from app.oauth import get_current_user
from sqlalchemy.orm import Session
from app.models import *
from fastapi_pagination import LimitOffsetPage, add_pagination, paginate


router = APIRouter(
	prefix='/profile',
	tags=['Following']
)

class Following(BaseModel):
	id: int
	user: str
	follower: str

# Profile Setting 
@router.get('/following/count')
def get_following_count(db: Session = Depends(get_db),
	current_user: TokenData =  Depends(get_current_user)):
	username = current_user.username
	following_list = db.query(Following).filter(follower=username).all()
	following_count = len(following_list)

	return {"message" : f"{username} has {following_count} followings"}



@router.get('/followers/count')
def get_followers_count(db: Session = Depends(get_db),
	current_user: TokenData =  Depends(get_current_user)):
	username = current_user.username
	followers_list = db.query(Following).filter(username=username).all()
	followers_count = len(followers_list)

	return {"message" : f"{username} has {followers_count} followers"}


# Followers names list
@router.get('/followers/names', response_model=LimitOffsetPage[Following])
def get_followers(skip: int = 0, limit: int = 30, db: Session = Depends(get_db),
	current_user: TokenData =  Depends(get_current_user)):

	username = current_user.username
	followers_list = db.query(Following).filter(user=username).offset(skip).limit(limit).all()
	user_names = []

	for user in followers_list:
		user_names.append(user.username)

	return {"followings": f"{user_names}"}



# Followings names list
# review
# skip: int = 0, limit: int = 100,
@router.get('/followings/names')
def get_followings(skip: int = 0, limit: int = 30, db: Session = Depends(get_db),
	current_user: TokenData =  Depends(get_current_user)):
	username = current_user.username
	following_list = db.query(Following).filter(follower=username).offset(skip).limit(limit).all()
	user_names = []

	for user in following_list:
		user_names.append(user.username)

	# return paginate(user_names)

	return {"followings": f"{user_names}"}



@router.get('/follow')
def toggle_follow(db: Session = Depends(get_db),
	current_user: TokenData =  Depends(get_current_user)):
	pass

# def follow_user(session: Session, user: User, following_user: User):
#     follow = Follow(user=user, following_user=following_user)
#     session.add(follow)
#     session.commit()

# def get_following(user: User):
#     return [follow.following_user for follow in user.following]