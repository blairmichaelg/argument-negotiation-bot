from typing import AsyncIterable, Dict, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os
import logging
import openai
import fastapi_poe as fp
from fastapi import FastAPI, Depends
from modal import Image, Stub, asgi_app

from utils.database import SessionLocal, User, get_db
from utils.external_api import fetch_salary_data
from utils.helpers import analyze_sentiment, generate_dynamic_follow_up_questions
from core import (
    handle_debate,
    handle_negotiation,
    handle_fact_check,
    handle_bias_detection,
    handle_contract_analysis,
    handle_salary_negotiation,
    handle_error,
    create_prompt,
    PROMPTS,
)
from utils.error_handling import validate_input

# --- Configuration ---
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./argument_negotiation_bot.db")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

def configure_logging():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("argument_negotiation_bot")
    return logger

logger = configure_logging()

# Global constants
MAX_INPUT_LENGTH = 1500
FUNCTIONALITY_KEYWORDS = {
    "debate": handle_debate,
    "negotiation": handle_negotiation,
    "fact-check": handle_fact_check,
    "cognitive bias": handle_bias_detection,
    "contract": handle_contract_analysis,
    "salary": handle_salary_negotiation,
}

# --- OpenAI Initialization ---
openai.api_key = OPENAI_API_KEY

# --- Pydantic Model for User Data ---
class UserData(BaseModel):
    user_id: int
    input_text: str

# --- Bot Class ---
class ArgumentNegotiationBot(fp.PoeBot):
    app = FastAPI()

    def __init__(self):
        super().__init__()
        self.app = FastAPI()

    async def handle_message(self, message: str, user_data: UserData, db: Session):
        try:
            validated_input = validate_input(message)
            prompt = create_prompt(validated_input, user_data)
            response = await openai.Completion.create(
                engine="davinci-codex",
                prompt=prompt,
                max_tokens=MAX_INPUT_LENGTH
            )
            return response.choices[0].text.strip()
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            return handle_error(e)

# --- FastAPI App ---
app = FastAPI()

@app.on_event("startup")
async def startup_event_handler():
    logger.info("Starting up the application...")
    # Add any startup logic here

@app.on_event("shutdown")
async def shutdown_event_handler():
    logger.info("Shutting down the application...")
    # Add any shutdown logic here

# PoeBot ASGI app
poe_bot = ArgumentNegotiationBot()
poe_bot.app = app

@app.post("/process")
async def process_message(user_data: UserData, db: Session = Depends(get_db)):
    return await poe_bot.handle_message(user_data.input_text, user_data, db)

app.mount("/poe", poe_bot.app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)