from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from typing import Optional, Union
from fastapi import File, UploadFile


class ProfileSchema(BaseModel):
	bio: str
	location: str

class UserResponseModel(BaseModel):
	id: int
	email: EmailStr
	username: str
	created_at: datetime

	class Config:
		orm_mode = True

class PostBase(BaseModel):
	title: str
	caption: str
	published: bool = True




class PostCreateInfo(PostBase): #infoSchema
	# image: bytes = Field(..., media_type="image/jpeg")
	# image: Union[UploadFile, None] = None
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

class PostResponseSchema(BaseModel): # response
	title: str
	content: str
	published: bool = True
	created_at: datetime

	class Config:
		orm_mode = True

	
class UserinfoSchema(BaseModel):
	username: str
	email: EmailStr  #ensures valid email
	password: str
	confirm_password: str



class LoginSchema(BaseModel):
	username: str
	email: EmailStr
	password: str 

class Token(BaseModel):
	access_token: str
	token_type: str
	token_type: str

class TokenData(BaseModel):
	id: Optional[str] = None
	email: Optional[str] = None
	username: str

class UpVoteSchema(BaseModel):
	post_id = str
	password: str 