from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.schema import LoginSchema, UserResponseModel, UserinfoSchema, Token , TokenData
from app.models import *
from app.utils import *
from .. import oauth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm




router = APIRouter(
	prefix='/auth',
	tags=['Authentication']
)



#LoginSchema
@router.post('/login', response_model=Token)
def login_for_token(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#def login_for_token(user_credentials: LoginSchema, db: Session = Depends(get_db)):

	user = db.query(User).filter(
		User.username == user_credentials.username).first()
	

	if not user:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
		detail=f'invalid Credentials')

	if not verify_password(user_credentials.password, user.password):
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
		detail=f'invalid Credentials')

	# creates token

	access_token = oauth.create_access_token(data= {"user_id": user.id, "user_email": user.email})

	# returns token
	return {'access_token': access_token, 'token_type': 'bearer'}

@router.post('/signup')
def signup(user: UserinfoSchema, db: Session = Depends(get_db)):

	if user.confirm_password == user.password:
		hashed_password = hash(user.password)
		user.password = hashed_password

		

		try:
			new_user = User(**user.dict())
			db.add(new_user)
			db.commit()
			return {"message": "you have been successfully signed up"}
		
		except:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
			detail=f'Duplicate Details')
	else:
		return f"passwords doesnt match"
