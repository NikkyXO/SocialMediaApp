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
	id 					= Column(Integer, primary_key=True, index=True, nullable=False)
	email 				= Column(String(100), nullable=False, unique=True)
	password 			= Column(String(100), nullable=False, unique=True)
	created_at 			= Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)
