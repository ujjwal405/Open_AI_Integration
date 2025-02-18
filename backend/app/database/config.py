from app.models.faq import Base
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load database URL from environment variables (default to local Postgres)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/dbname")

# Create database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def init_db():
    Base.metadata.create_all(bind=engine)
