from jose import JWTError, jwt
from datetime import  timedelta
from .utils import verify_password
import datetime
from .schema import *
from .database import *
from fastapi import FastAPI, Response, Depends, HTTPException, status, Security
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from .models import *
from .config import settings
from typing import Union

security = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

# needed: secret key, algo, expiration time

SECRET_KEY = "95ec0365b7f813481a5925ba5d8ca4e39f657bd82116665d55cf7da53f06f576"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# SECRET_KEY = settings.secret_key
# ALGORITHM = settings.algorithm
# ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

class TokenData(BaseModel):
    username: Union[str, None] = None

def get_user(email: str, db: Session = Depends(get_db)):

	return db.query(User).filter(User.email == email).first()




def create_access_token(data: dict):
	to_encode = data.copy()

	expire = datetime.datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	to_encode.update({"exp": expire})

	encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

	return encoded_jwt


def verify_access_token(token: str, credentials_exception):

	try:
		payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])

		# id: str = payload.get('user_id')
		email: str = payload.get('email')

		if email is None:
			raise credentials_exception

		# verifies / validates if id passed is same as payload id
		# review
		token_data = TokenData(email=email)

	except JWTError:
		raise credentials_exception

	return token_data

def authenticate_user(db: Session, email: str, password: str):
	user = get_user(db, email)
	if not user:
		return False

	if not verify_password(password, user.password):
		return False

	return user

def get_current_user(token: HTTPAuthorizationCredentials= Depends(security), db: Session = Depends(get_db)):


	credentials_exception = HTTPException(
		status_code= status.HTTP_401_UNAUTHORIZED,
		detail=f'Could not validate credentials', 
		headers={'WWW-Authenticate': 'Bearer'}
	)
	token = token.credentials

	try:
		payload = jwt.decode(token, settings.secret_key,
								algorithms=[settings.algorithm])

		# print("payload => ", payload)

		user_email: str = payload.get("user_email")
		if user_email is None:
			raise credentials_exception

	except JWTError:
		raise credentials_exception
	user = get_user(email=user_email, db=db)
	if user is None:
		raise credentials_exception
	return user
