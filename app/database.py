from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:PuI9XJ0u3Q7yRebsq8k0@containers-us-west-96.railway.app:7307/railway'

#SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# SQLALCHEMY_DATABASE_URL = 'mysql+mysqldb://username:password@localhost/db_name'
#SQLALCHEMY_DATABASE_URL = f'mysql+mysqldb://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
	db = sessionLocal()

	try:
		yield db
	finally:
		db.close()

Base.metadata.create_all(bind=engine)