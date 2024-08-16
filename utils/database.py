from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Database URL from environment variable
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite:///./argument_negotiation_bot.db"
)

# Create the database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()


class User(Base):
    """
    User model for storing user-related data in the database.

    Attributes:
        id (int): Primary key for the user.
        poe_user_id (str): Unique identifier for the user.
        interaction_history (str): History of user interactions.
        preferences (str): User preferences stored as a JSON string.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    poe_user_id = Column(String, unique=True, index=True)
    interaction_history = Column(Text, default="")
    preferences = Column(Text, default="{}")


# Create all tables in the database
Base.metadata.create_all(bind=engine)


def get_db():
    """
    Dependency function that provides a database session.

    Yields:
        Session: A database session for use in operations.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
