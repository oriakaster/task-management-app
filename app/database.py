from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Purpose: Sets up the database connection and session management for the application
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}, 
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency

def get_db():
    """input: None
    output: Yields a database session for use in requests.
    purpose: Provides a session to interact with the database, ensuring it is closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()