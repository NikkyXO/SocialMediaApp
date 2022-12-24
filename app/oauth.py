from jose import JWTError, jwt
from datetime import  timedelta
import datetime
from .schema import *
from .database import *
from fastapi import FastAPI, Response, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from .models import *


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

# needed: secret key, algo, expiration time

SECRET_KEY = "95ec0365b7f813481a5925ba5d8ca4e39f657bd82116665d55cf7da53f06f576"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# SECRET_KEY = settings.secret_key
# ALGORITHM = settings.algorithm
# ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes



def get_user(email: str, db: Session = Depends(get_db)):

	return db.query(User).filter(User.email == email).first()




def create_access_token(data: dict):
	to_encode = data.copy()

	expire = datetime.datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	to_encode.update({"exp": expire})

	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

	return encoded_jwt


def verify_access_token(token: str, credentials_exception):

	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

		id: str = payload.get('user_id')
		email: str = payload.get('email')

		if id is None or email is None:
			raise credentials_exception

		# verifies / validates if id passed is same as payload id
		token_data = TokenData(id=id, email=email)

	except JWTError:
		raise credentials_exception

	return token_data

def get_current_user(token: str = Depends(
	oauth2_scheme), db: Session = Depends(get_db)):

	credentials_exception = HTTPException(
		status_code= status.HTTP_401_UNAUTHORIZED,
		detail=f'Could not validate credentials', 
		headers={'WWW-Authenticate': 'Bearer'}
	)

	token_data = verify_access_token(token, credentials_exception)

	user = get_user(email=token_data.email, db=db)
	if not user:
		return credentials_exception
