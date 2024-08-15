import asyncio
import logging
import os
from typing import AsyncIterable, Dict, Optional

import fastapi_poe as fp
from modal import Image, Stub, asgi_app
from pydantic import BaseModel

import openai
from utils.database import User, get_db, SessionLocal
from utils.external_api import fetch_salary_data
from utils.helpers import analyze_sentiment, generate_dynamic_follow_up_questions

from core import (
    handle_debate,
    handle_negotiation,
    handle_fact_check,
    handle_bias_detection,
    handle_contract_analysis,
    handle_salary_negotiation,
)
from utils.error_handling import handle_error, validate_input
from utils.prompt_engineering import create_prompt

# --- Configuration ---
DATABASE_URL = os.environ.get("DATABASE_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

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
    poe_user_id: str
    interaction_history: Optional[str] = None
    preferences: Optional[dict] = None

# --- Bot Class ---
class ArgumentNegotiationBot(fp.PoeBot):
    def __init__(self):
        super().__init__()
        self.ongoing_dialogues: Dict[str, Dict] = {}  

    async def get_response(
        self, request: fp.QueryRequest
    ) -> AsyncIterable[fp.PartialResponse]:
        """Handles user queries, routing to functionalities and managing dialogue."""
        try:
            user_input = validate_input(
                request.query[-1].content.lower(), MAX_INPUT_LENGTH
            )
            poe_user_id = request.sender_user_id
            logger.info(f"User Input: {user_input} (User: {poe_user_id})")

            # --- User Profile Management ---
            user_data = await self.get_or_create_user(poe_user_id)
            user_data.interaction_history += f"\nUser: {user_input}"

            # --- Sentiment Analysis ---
            sentiment = await analyze_sentiment(user_input)
            logger.info(f"Sentiment: {sentiment}")
            # ... (Use sentiment to tailor responses - more on this later)

            # --- Functionality Routing ---
            for keyword, handle_func in FUNCTIONALITY_KEYWORDS.items():
                if keyword in user_input:
                    async for response in await handle_func(
                        request, user_input, user_data
                    ):
                        yield response

                    # --- Dynamic Follow-up Questions ---
                    follow_up_questions = await generate_dynamic_follow_up_questions(
                        keyword, user_input, user_data.interaction_history
                    )
                    if follow_up_questions:
                        yield fp.PartialResponse(
                            text="\n\nDo you want to explore any of these?\n"
                            + "\n".join(follow_up_questions)
                        )

                    # --- Dialogue Management (Example) ---
                    self.ongoing_dialogues[
                        poe_user_id
                    ] = {  # Store dialogue context
                        "functionality": keyword,
                        "history": user_input,
                    }
                    return

            yield fp.PartialResponse(
                text="I'm not sure I understand. Please specify what you'd like me to do. Available options include: debate, negotiation, fact-check, cognitive bias analysis, contract analysis, or salary negotiation."
            )

        except Exception as e:
            logger.exception("An error occurred:")
            yield await handle_error(e)

        finally:
            # Update user data in the database
            await self.update_user_data(user_data)

    # ... (other methods)

    async def get_or_create_user(self, poe_user_id: str) -> UserData:
        """Retrieves or creates a user profile."""
        async with SessionLocal() as db:
            user = db.query(User).filter_by(poe_user_id=poe_user_id).first()
            if user:
                return UserData(
                    poe_user_id=user.poe_user_id,
                    interaction_history=user.interaction_history,
                    preferences=json.loads(user.preferences),
                )
            else:
                new_user = User(poe_user_id=poe_user_id, interaction_history="", preferences="{}")
                db.add(new_user)
                db.commit()
                return UserData(poe_user_id=poe_user_id, interaction_history="", preferences={})

    async def update_user_data(self, user_data: UserData):
        """Updates user data in the database."""
        async with SessionLocal() as db:
            user = db.query(User).filter_by(poe_user_id=user_data.poe_user_id).first()
            if user:
                user.interaction_history = user_data.interaction_history
                user.preferences = json.dumps(user_data.preferences)
                db.commit()

    async def get_settings(self, setting: fp.SettingsRequest) -> fp.SettingsResponse:
        """Defines bot settings for Poe."""
        return fp.SettingsResponse(
            server_bot_dependencies={
                "GPT-3.5-Turbo": 5,
                "Claude-instant": 3,
                "GPT-4": 2,
            },
            allow_attachments=True,
            expand_text_attachments=True,
            enable_image_comprehension=False,  # Consider enabling in the future
            introduction_message="Welcome to the Argument & Negotiation Master Bot! How can I assist you today? You can ask for help with debates, negotiations, fact-checking, cognitive bias detection, contract analysis, or salary negotiation.",
            enable_multi_bot_chat_prompting=True,
        )


# --- Modal Deployment Configuration ---
REQUIREMENTS = [
    "fastapi-poe==0.0.36",
    "modal-client",
    "pydantic",
    "python-dotenv",
    "requests",
    "sqlalchemy",
    "openai"
]
image = Image.debian_slim().pip_install(*REQUIREMENTS)
stub = Stub("argument-negotiation-bot")


@stub.function(image=image)
@asgi_app()
def fastapi_app():
    bot = ArgumentNegotiationBot()
    app = fp.make_app(bot, allow_without_key=True)
    return app


if __name__ == "__main__":
    asyncio.run(fastapi_app())