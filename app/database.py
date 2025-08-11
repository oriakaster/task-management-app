from sqlalchemy import create_engine, make_url
from sqlalchemy.orm import sessionmaker, declarative_base
from .core.settings import get_settings

# Purpose: Sets up the database connection and session management for the application
settings = get_settings()
DATABASE_URL = settings.database_url

def _connect_args(url: str) -> dict:
    """input: Database URL as a string
       output: Dictionary of connection arguments for SQLAlchemy
       Parses the URL to determine if any specific connection arguments are needed."""
    try:
        u = make_url(url)
        return {"check_same_thread": False} if u.drivername.startswith("sqlite") else {}
    except Exception:
        # if parsing fails, play it safe and send no extra args
        return {}

engine = create_engine(DATABASE_URL, connect_args=_connect_args(DATABASE_URL))
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