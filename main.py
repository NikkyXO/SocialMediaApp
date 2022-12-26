from fastapi import FastAPI, Response, status
from app.models import *
from app.routers import post, user, auth
from fastapi.middleware.cors import CORSMiddleware
from app.database import *
from app.config import settings


import sys
sys.path.append('..')

# description of the social media app
description= ""

app = FastAPI(
	title="Social Media",
	description=description,
	# swagger_ui_parameters={operationsSorter: "method"}
)

origins = ['*', 'http://localhost:3000/']

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=['*'],
	allow_headers=['*']
)



@app.get('/')
def root(): 
	return {'message': 'Hello, world!'}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

Base.metadata.create_all(bind=engine)

	