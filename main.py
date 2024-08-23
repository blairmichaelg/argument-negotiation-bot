# File: main.py

import os
import logging
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uvicorn
import openai

from core import (
    handle_debate,
    handle_negotiation,
    handle_fact_check,
    handle_bias_detection,
    handle_contract_analysis,
    handle_salary_negotiation,
)
from utils.error_handling import handle_error, validate_input
from utils.database import get_db
import fastapi_poe as fp

# --- Configuration ---
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./argument_negotiation_bot.db")
OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY",
    "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",
)

# --- Logging Configuration ---


def configure_logging():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("argument_negotiation_bot")
    return logger


logger = configure_logging()

# --- Global Constants ---
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
    def __init__(self):
        super().__init__()
        self.app = FastAPI()
        self.request = None  # Define the 'request' attribute
        self.user_data = {}  # Define the 'user_data' attribute

    async def handle_message(self, message: str):
        try:
            validated_input = validate_input(message)
            messages = []
            for keyword, handler in FUNCTIONALITY_KEYWORDS.items():
                if keyword in validated_input.lower():
                    async for msg in handler(
                        request=fp.QueryRequest(
                            version="",
                            type="query",
                            query=[],
                            user_id="",
                            conversation_id="",
                            message_id="",
                        ),
                        user_input=validated_input,
                        user_data=self.user_data,
                    ):
                        messages.append(msg)
                    return messages
            messages.append(
                fp.PartialResponse(
                    text="I'm sorry, I didn't understand your request. Can you specify which feature you'd like to use?"
                )
            )
            return messages
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            return [await handle_error(e)]

    async def get_settings(self, setting: fp.SettingsRequest) -> fp.SettingsResponse:
        return fp.SettingsResponse(
            server_bot_dependencies={
                "GPT-3.5-Turbo": 5,
                "Claude-instant": 3,
                "GPT-4": 2,
            },
            allow_attachments=True,
            expand_text_attachments=True,
            enable_image_comprehension=False,
            introduction_message="Welcome to the Argument and Negotiation Master Bot. How can I assist you today?",
            enable_multi_bot_chat_prompting=True,
        )


# --- FastAPI App ---


app = FastAPI()

# --- Startup and Shutdown Event Handlers ---


@app.on_event("startup")
async def startup_event_handler():
    logger.info("Starting up the application...")
    # Add any startup logic here


@app.on_event("shutdown")
async def shutdown_event_handler():
    logger.info("Shutting down the application...")
    # Add any shutdown logic here


# --- PoeBot ASGI App ---
poe_bot = ArgumentNegotiationBot()
poe_bot.app = app

# --- Module-level variable for database dependency ---
db_dependency = Depends(get_db)

# --- FastAPI Route for Processing Messages ---


@app.post("/process")
async def process_message(user_data: UserData, db: Session = db_dependency):
    return await poe_bot.handle_message(user_data.input_text)


# --- Mount PoeBot ASGI App ---
app.mount("/poe", poe_bot.app)

# --- Run the FastAPI App ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
