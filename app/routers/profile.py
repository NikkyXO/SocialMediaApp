from app.schema import *
from fastapi import FastAPI, Response, Depends, HTTPException, status, APIRouter
from app.database import get_db
from app.oauth import get_current_user
from app.models import *
from sqlalchemy.orm import Session
from fastapi import File, UploadFile
import shutil
import os
from app.utils import save_upload_file

router = APIRouter(
	prefix='/profile',
	tags=['Settings']
)



# Profile Setting   
@router.post('/settings')
def profile_setting(bio: str, address: str, 
	profile_image: UploadFile = File(...) ,db: Session = Depends(get_db),
	current_user: TokenData =  Depends(get_current_user)): 
	

	filepath = save_upload_file(profile_image)
	print(filepath)

	user_id = current_user.id

	

	new_profile = Profile(profile_image=filepath, bio=bio, address=address, owner_id=user_id)
	db.add(new_profile)
	db.commit()

	return {"message": f"Profile created successfully"}

# endpoint for retreiving profile information