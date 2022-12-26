from fastapi import FastAPI
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str = '0.0.0.0'

    database_password: str = '410208olA$$$'
    database_name: str = 'socials_db'
    database_username = 'root'
    secret_key: str = '95ec0365b7f813481a5925ba5d8ca4e39f657bd82116665d55cf7da53f06f576'
    algorithm: str = "HS256" 
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()