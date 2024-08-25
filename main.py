import os
import logging
from typing import AsyncIterable

import openai
from fastapi import FastAPI
from modal import Image, Stub, asgi_app, Secret
import fastapi_poe as fp

from core import (
    handle_debate,
    handle_negotiation,
    handle_fact_check,
    handle_bias_detection,
    handle_contract_analysis,
    handle_salary_negotiation,
)
from utils.error_handling import handle_error, validate_input

# --- Configuration ---
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", Secret.from_name("OPENAI_API_KEY"))

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("argument-negotiation-bot")

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


# --- Bot Class ---
class ArgumentNegotiationBot(fp.PoeBot):
    def __init__(self):
        super().__init__()
        self.app = app

    async def get_response(
        self, request: fp.QueryRequest
    ) -> AsyncIterable[fp.PartialResponse]:
        user_input = request.query[-1].content.lower()

        try:
            validated_input = validate_input(user_input)

            for keyword, handler in FUNCTIONALITY_KEYWORDS.items():
                if keyword in validated_input:
                    async for msg in handler(request, validated_input):
                        yield msg
                    return

            yield fp.PartialResponse(
                text="I'm sorry, I didn't understand your request. Can you specify which feature you'd like to use?"
            )
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            yield await handle_error(e)

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

# --- PoeBot Instance ---
poe_bot = ArgumentNegotiationBot()
poe_bot.app = app

# --- Modal Setup ---
REQUIREMENTS = [
    "fastapi-poe==0.0.47",
    "openai",
    "sqlalchemy",
    "uvicorn",
    "psycopg2-binary",
    "nltk",
    "cachetools",
    "aiohttp",
]
image = Image.debian_slim().pip_install(*REQUIREMENTS).apt_install("libpq-dev")
stub = Stub("argument-negotiation-bot")


@stub.function(
    image=image,
    secrets=[
        Secret.from_name("DATABASE_URL"),
        Secret.from_name("OPENAI_API_KEY"),
        Secret.from_name("ADZUNA_API_ID"),
        Secret.from_name("ADZUNA_API_KEY"),
    ],
)
@asgi_app()
def fastapi_app():
    return app


# --- Mount PoeBot ASGI App ---
app.mount("/poe", poe_bot.app)

# --- Run the FastAPI App (for local testing) ---
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
