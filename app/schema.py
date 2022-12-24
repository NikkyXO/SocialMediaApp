from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from typing import Optional




class UserResponseModel(BaseModel): # user response
	id: int
	email: EmailStr
	created_at: datetime

	class Config:
		orm_mode = True

class PostBase(BaseModel):
	title: str
	content: str
	published: bool = True


class PostCreateInfo(PostBase): #infoSchema
	pass

class Postin(PostBase): # post Response
	id: int
	created_at: datetime
	owner_id: int
	owner: UserResponseModel

	class Config:
		orm_mode = True

class PostOut(BaseModel):
    Post: Postin
    votes: int

class ResponseSchema(BaseModel): # response
	title: str
	content: str
	published: bool = True
	id: int
	created_at: datetime

	class Config:
		orm_mode = True

	
class UserinfoSchema(BaseModel):
	email: EmailStr  #ensures valid email
	password: str



class LoginSchema(BaseModel):
	email: EmailStr
	password: str 

class Token(BaseModel):
	access_token: str
	token_type: str

class TokenData(BaseModel):
	id: Optional[str] = None
	email: Optional[str] = None 
