"""
database.py
-----------
Sets up the SQLite database engine and session factory.
Provides a dependency-injectable session for use in routers.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# SQLite database file will be created in the project root
DATABASE_URL = "sqlite:///./library.db"

# connect_args is required for SQLite to work with FastAPI's async threads
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Each request gets its own session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base class for all ORM models
class Base(DeclarativeBase):
    pass


def get_db():
    """
    Dependency function that provides a database session.
    Automatically closes the session after the request is done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
