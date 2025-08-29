# db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import logging   #1st change

logger = logging.getLogger(__name__)
#2nd change

# Load .env file
load_dotenv()

# Pick DB URL (local vs docker)
DATABASE_URL = os.getenv("DATABASE_URL_LOCAL") or os.getenv("DATABASE_URL")
logger.info(f"Using database URL: {DATABASE_URL}")    #3rd change


# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Base class
Base = declarative_base()

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency for FastAPI routes
def get_db():
    logger.debug("Creating new database session") #4th change
    db = SessionLocal()
    try:
        yield db
    finally:
        logger.debug("Closing database session") #5th change
        db.close()


