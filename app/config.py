from dotenv import load_dotenv
from pydantic import BaseSettings
load_dotenv()

class Settings(BaseSettings):
    database_hostname: str 

    database_password: str 
    database_name: str
    database_username : str
    secret_key: str 
    algorithm: str 
    database_port: str 
    access_token_expire_minutes: int = 30
    # app_passwd: str
    # app_email: str

    class config:
        env_file = ".env"


settings = Settings()