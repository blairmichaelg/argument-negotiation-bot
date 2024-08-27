import logging

import fastapi_poe as fp
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from modal import Image, Secret, Stub, asgi_app

from core import (
    handle_bias_detection,
    handle_contract_analysis,
    handle_debate,
    handle_fact_check,
    handle_negotiation,
    handle_salary_negotiation,
)
from utils.error_handling import handle_error

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()


# PoeBot class
class ArgumentNegotiationBot(fp.PoeBot):
    async def get_response(self, request: fp.QueryRequest):
        user_input = request.query[-1].content.lower()

        functionality_map = {
            "debate": handle_debate,
            "negotiation": handle_negotiation,
            "fact-check": handle_fact_check,
            "cognitive bias": handle_bias_detection,
            "contract": handle_contract_analysis,
            "salary": handle_salary_negotiation,
        }

        for key, handler in functionality_map.items():
            if key in user_input:
                async for msg in handler(request, user_input):
                    yield msg
                return

        yield fp.PartialResponse(
            text="I'm sorry, I didn't understand your request. Can you specify which feature you'd like to use?"
        )

    async def get_settings(self, setting: fp.SettingsRequest):
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


# Define a deployment-ready function
REQUIREMENTS = [
    "fastapi-poe==0.0.47",
    "sqlalchemy",
    "pydantic",
    "requests",
    "cachetools",
    "aiohttp",
    "nltk",
]
image = Image.debian_slim().pip_install(*REQUIREMENTS)
stub = Stub("argument-negotiation-bot")


@stub.function(
    image=image,
    secrets=[
        Secret.from_name("ADZUNA_API_ID"),
        Secret.from_name("ADZUNA_API_KEY"),
        Secret.from_name("DATABASE_URL"),
    ],
)
@asgi_app()
def fastapi_app():
    bot = ArgumentNegotiationBot()
    app = fp.make_app(bot, allow_without_key=True)
    return app


# Error handler
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    response = await handle_error(exc)
    return JSONResponse(
        status_code=500,
        content={"message": response.text},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
