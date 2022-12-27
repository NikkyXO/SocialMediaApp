from .database import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime
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
	title 				= Column(String(100), nullable=False, unique=True)
	content 			= Column(String(1024), nullable=False)
	published 			= Column(Boolean, default=False, nullable=False)
	created_at 			= Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
	rating				= Column(Integer, default=0, nullable=True)
	owner_id			= Column(Integer, ForeignKey(
		'users.id', ondelete='CASCADE'), nullable=False)

class User(Base):
	__tablename__ = 'users'
	__table_args__ = {"extend_existing": True}

	id 					= Column(Integer, primary_key=True, index=True, nullable=False)
	username 			= Column(String(100), nullable=False, unique=True)
	email 				= Column(String(100), nullable=False, unique=True)
	password 			= Column(String(100), nullable=False, unique=True)
	created_at 			= Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)

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

	post_id 			= post_id = Column(Integer, ForeignKey(
						"posts.id", ondelete="CASCADE"), primary_key=True)
	id  				= Column(Integer, primary_key=True, index=True, nullable=False)
	username			= Column(String(100), nullable=False, unique=True)
	body				= Column(String(100), nullable=False, unique=True)
	created_at			= Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)


class CommentResponse(Base):
	__tablename__ = 'commentResponse'
	__table_args__ = {"extend_existing": True}

	post_id 			= post_id = Column(Integer, ForeignKey(
						"posts.id", ondelete="CASCADE"), primary_key=True)
	id  				= Column(Integer, primary_key=True, index=True, nullable=False)
	username			= Column(String(100), nullable=False, unique=True)
	body				= Column(String(100), nullable=False, unique=True)
	created_at			= Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
	self_: bool 		= Column(Boolean, default=False, nullable=False)