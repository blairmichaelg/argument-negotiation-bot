import os

from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# from modal.secret import Secret

# Database URL from Modal secrets - REPLACE WITH YOUR ACTUAL DATABASE URL
# For now, you can use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./test.db")

# Create the database engine
if str(SQLALCHEMY_DATABASE_URL).startswith("sqlite:///./"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

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


class NegotiationScenario(Base):
    """
    Model for storing negotiation scenarios.

    Attributes:
        id (int): Primary key for the scenario.
        topic (str): The topic of the negotiation.
        user_offers (str): A JSON string representing the user's offers.
        bot_responses (str): A JSON string representing the bot's responses.
    """

    __tablename__ = "negotiation_scenarios"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=False)
    user_offers = Column(Text, default="[]")
    bot_responses = Column(Text, default="[]")


# Create all tables in the database - ONLY IF THEY DON'T EXIST
Base.metadata.create_all(bind=engine, checkfirst=True)


async def get_db():
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


async def create_user(db, poe_user_id: str):
    """Creates a new user in the database."""
    new_user = User(poe_user_id=poe_user_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def get_user_by_id(db, poe_user_id: str):
    """Retrieves a user from the database by their Poe user ID."""
    return db.query(User).filter(User.poe_user_id == poe_user_id).first()


async def update_user_preferences(db, poe_user_id: str, preferences: dict):
    """Updates a user's preferences in the database."""
    user = db.query(User).filter(User.poe_user_id == poe_user_id).first()
    if user:
        user.preferences = preferences
        db.commit()
        db.refresh(user)
        return user
    else:
        return None


async def create_negotiation_scenario(db, topic: str):
    """Creates a new negotiation scenario in the database."""
    new_scenario = NegotiationScenario(topic=topic)
    db.add(new_scenario)
    db.commit()
    db.refresh(new_scenario)
    return new_scenario


async def get_negotiation_scenario_by_id(db, scenario_id: int):
    """Retrieves a negotiation scenario from the database by its ID."""
    return (
        db.query(NegotiationScenario)
        .filter(NegotiationScenario.id == scenario_id)
        .first()
    )


async def update_negotiation_scenario(
    db, scenario_id: int, user_offers: list, bot_responses: list
):
    """Updates a negotiation scenario in the database."""
    scenario = (
        db.query(NegotiationScenario)
        .filter(NegotiationScenario.id == scenario_id)
        .first()
    )
    if scenario:
        scenario.user_offers = user_offers
        scenario.bot_responses = bot_responses
        db.commit()
        db.refresh(scenario)
        return scenario
    else:
        return None
