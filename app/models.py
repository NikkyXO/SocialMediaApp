from .database import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime, BLOB
from sqlalchemy.orm import relationship
from uuid import uuid4
import time
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
import datetime


class Post(Base):
	__tablename__ = 'posts'
	__table_args__ = {'extend_existing': True}

	id 					= Column(Integer, primary_key=True, index=True, nullable=False)
	caption 			= Column(String(1024), nullable=False)
	published 			= Column(Boolean, default=False, nullable=False)
	created_at 			= Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
	rating				= Column(Integer, default=0, nullable=True)
	owner_id			= Column(Integer, ForeignKey(
		'users.id', ondelete='CASCADE'), nullable=False)
	image 				= Column(String(100), nullable=False, default=None)

class Profile(Base):
	__tablename__ = 'profile'
	__table_args__ = {'extend_existing': True}

	id 					= Column(Integer, primary_key=True, index=True, nullable=False)
	bio 				= Column(String(1024), nullable=False)
	published 			= Column(Boolean, default=False, nullable=False)
	created_at 			= Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
	address 			= Column(String(1024), nullable=False)
	owner_id			= Column(Integer, ForeignKey(
		'users.id', ondelete='CASCADE'), nullable=False)
	profile_image 		= Column(BLOB, nullable=True, default=None)

class User(Base):
	__tablename__ = 'users'
	__table_args__ = {"extend_existing": True}

	id 					= Column(Integer, primary_key=True, index=True, nullable=False)
	username 			= Column(String(100), nullable=False, unique=True)
	email 				= Column(String(100), nullable=False, unique=True)
	password 			= Column(String(100), nullable=False, unique=True)
	created_at 			= Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
	# followers 			= relationship("Follow", back_populates="follower_user")
	# following 			= relationship("Follow", back_populates="following_user")
	
class Vote(Base):
	__tablename__ = "votes"
	user_id 			= Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
	post_id 			= Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)


class PostResponse(Base):
	__tablename__ = 'postResponses'
	__table_args__ = {"extend_existing": True}

	username 			= Column(String(100), nullable=False, unique=True)
	id 					= Column(Integer, primary_key=True, index=True, nullable=False)
	body				= Column(String(100), nullable=False, unique=True)
	created_at			= Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
	avatar				= Column(String(100), nullable=False, unique=True)
	post_id				= Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)


class Comment(Base):
	__tablename__ = 'comments'
	__table_args__ = {"extend_existing": True}
	post_id 			= post_id = Column(Integer, ForeignKey(
						"posts.id", ondelete="CASCADE"))
	comment_id  		= Column(Integer, primary_key=True, nullable=False)
	username			= Column(String(100), nullable=False, unique=True)
	body				= Column(String(100), nullable=False, unique=True)
	created_at			= Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)

class Following(Base):
	__tablename__ = 'followings'
	id 						= Column(Integer, primary_key=True, nullable=False)
	user					= Column(String(100), nullable=True, unique=False)
	Follower				= Column(String(100), nullable=True, unique=False)

	# id 						= Column(Integer, primary_key=True, nullable=False)
	# user_id 					= Column(Integer, ForeignKey('users.id'))
	# following_user_id 		= Column(Integer, ForeignKey('users.id'))
	# following_user 			= relationship("User", back_populates="following", foreign_keys=[following_user_id])
	# follower_user 			= relationship("User", back_populates="followers", foreign_keys=[user_id])

class LikePost(Base):

	__tablename__ = 'likeposts'

	id 						= Column(Integer, primary_key=True, nullable=False)
	post_id 				= Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
	username				= Column(String(100))

# class CommentResponse(Base):
# 	__tablename__ = 'commentResponse'
# 	__table_args__ = {"extend_existing": True}

# 	post_id 			= post_id = Column(Integer, ForeignKey(
# 						"posts.id", ondelete="CASCADE"), primary_key=True)
# 	id  				= Column(Integer, primary_key=True, index=True, nullable=False)
# 	username			= Column(String(100), nullable=False, unique=True)
# 	body				= Column(String(100), nullable=False, unique=True)
# 	created_at			= Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
# 	self_: bool 		= Column(Boolean, default=False, nullable=False)