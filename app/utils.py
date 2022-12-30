from passlib.context import CryptContext
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable
from fastapi import UploadFile
import os

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash(password: str):
	return pwd_context.hash(password)

def verify_password(plain_password, hashedPassword):
	return pwd_context.verify(plain_password, hashedPassword)

# Handling file uploads

def save_upload_file(upload_file: UploadFile ):

	file_location = os.path.join('files', upload_file.filename)
	try:
		with open(file_location, "wb+") as file_object:
			file_object.write(upload_file.file.read())
	finally:
		upload_file.file.close()
	filepath = str.encode(file_location)
	return filepath




# def save_upload_file_tmp(upload_file: UploadFile) -> Path:
#     try:
#         suffix = Path(upload_file.filename).suffix
#         with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
#             shutil.copyfileobj(upload_file.file, tmp)
#             tmp_path = Path(tmp.name)
#     finally:
#         upload_file.file.close()
#     return tmp_path


def handle_upload_file(
    upload_file: UploadFile, handler: Callable[[Path], None]) -> None:
    tmp_path = save_upload_file_tmp(upload_file)
    try:
        handler(tmp_path)  # Do something with the saved temp file
    finally:
        tmp_path.unlink()  # Delete the temp file