import asyncio
from typing import AsyncIterable

import fastapi_poe as fp
from modal import Image, Stub, asgi_app

from core import (
    handle_debate,
    handle_negotiation,
    handle_fact_check,
    handle_bias_detection,
    handle_contract_analysis,
    handle_salary_negotiation,
)
from utils.error_handling import handle_error, validate_input
from utils.prompt_engineering import create_prompt, generate_follow_up_questions

class ArgumentNegotiationBot(fp.PoeBot):
    async def get_response(
        self, request: fp.QueryRequest
    ) -> AsyncIterable[fp.PartialResponse]:
        try:
            user_input = validate_input(request.query[-1].content.lower())

            functionality_map = {
                "debate": handle_debate,
                "negotiation": handle_negotiation,
                "fact-check": handle_fact_check,
                "cognitive bias": handle_bias_detection,
                "contract": handle_contract_analysis,
                "salary": handle_salary_negotiation,
            }

            for key, handle_func in functionality_map.items():
                if key in user_input:
                    prompt = create_prompt(key, topic=user_input)
                    async for msg in handle_func(request, prompt):
                        yield msg
                    
                    follow_up_questions = generate_follow_up_questions(key, user_input)
                    yield fp.PartialResponse(text="\n\nWould you like to explore any of these follow-up questions?\n" + "\n".join(follow_up_questions))
                    return

            yield fp.PartialResponse(
                text="I'm sorry, I didn't understand your request. Can you specify which feature you'd like to use? Available options are: debate, negotiation, fact-check, cognitive bias analysis, contract analysis, or salary negotiation."
            )

        except Exception as e:
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
            introduction_message="Welcome to the Argument and Negotiation Master Bot. How can I assist you today? You can ask for help with debates, negotiations, fact-checking, cognitive bias detection, contract analysis, or salary negotiation.",
            enable_multi_bot_chat_prompting=True,
        )

# Requirements and Modal setup
REQUIREMENTS = [
    "fastapi-poe==0.0.36",
    "modal-client",
    "pydantic",
    "python-dotenv",
]
image = Image.debian_slim().pip_install(*REQUIREMENTS)
stub = Stub("argument-negotiation-bot")

@stub.function(image=image)
@asgi_app()
def fastapi_app():
    bot = ArgumentNegotiationBot()
    app = fp.make_app(bot, allow_without_key=True)
    return app

# Main entry point
if __name__ == "__main__":
    asyncio.run(fastapi_app())