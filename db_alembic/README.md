Generic single-database configuration.

pip install alembic
alembic init alembic

# in env.py
from model import Base
target_metadata = [Base.metadata]

alembic revision --autogenerate -m "First commit"
alembic upgrade head