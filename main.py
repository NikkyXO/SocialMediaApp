from fastapi import FastAPI, Response, status, Request
from app.models import *
from app.routers import post, user, auth, profile, follows
from fastapi.middleware.cors import CORSMiddleware
from app.database import *
from app.config import settings
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.routing import Route, Mount
from starlette.applications import Starlette

templates = Jinja2Templates(directory='templates')
async def homepage(request):
    return templates.TemplateResponse('base.html', {'request': request})

routes = [
    Route('/', endpoint=homepage),
    Mount('/static', StaticFiles(directory='static'), name='static')
]

app = Starlette(debug=True, routes=routes)

import sys
sys.path.append('..')

# description of the social media app
description= ""

app = FastAPI(
	title="Social Media",
	description=description,
	# swagger_ui_parameters={operationsSorter: "method"}
)


app.mount("/static", StaticFiles(directory="static"), name="static")


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
app.include_router(profile.router)
app.include_router(follows.router)

Base.metadata.create_all(bind=engine)
	