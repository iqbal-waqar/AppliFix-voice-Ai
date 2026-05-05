from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from config import settings

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

Base = declarative_base()
