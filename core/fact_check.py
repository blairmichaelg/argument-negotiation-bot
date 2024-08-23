from typing import AsyncIterable
import fastapi_poe as fp
from fastapi_poe import (
    BotError,
    PartialResponse,
    QueryRequest,
)
import logging

from core.bias_detection import get_user_choice
from prompt_engineering import create_prompt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def fact_check(
    statement: str, request: QueryRequest
) -> AsyncIterable[PartialResponse]:
    """
    Suggest related facts or context for further exploration based on this statement.
    """
    async for msg in fp.stream_request(
        request, "GPT-3.5-Turbo", create_prompt("fact-check", topic=statement)
    ):
        yield PartialResponse(text=msg.text)


async def handle_fact_check(
    request: fp.QueryRequest, user_input: str, user_data: dict
) -> AsyncIterable[fp.PartialResponse]:
    """
    Handle the fact-checking process.
    """
    statement = user_input.replace("fact-check", "").strip()
    if not statement:
        raise BotError("Please provide a statement to fact-check.")

    yield fp.PartialResponse(text="Fact-checking the statement...\n\n")

    async for response in fact_check(statement, request):
        yield response

    yield fp.PartialResponse(text="\n\nWould you like to:\n")
    yield fp.PartialResponse(text="1. Explore additional sources?\n")
    yield fp.PartialResponse(text="2. Fact-check another statement?\n")
    yield fp.PartialResponse(text="3. Do something else?")

    # Handle user choice for further actions
    user_choice = await get_user_choice(
        request
    )  # Implement this function based on your framework
    if "1" in user_choice or "explore" in user_choice.lower():
        yield fp.PartialResponse(
            text="Okay, here are some additional sources to consider.\n\n"
        )
        async for msg in fp.stream_request(
            request, "GPT-4", create_prompt("fact-check", topic=statement)
        ):
            yield fp.PartialResponse(text=msg.text)
    elif "2" in user_choice or "fact-check" in user_choice.lower():
        yield fp.PartialResponse(text="Okay, please provide the new statement.")
    else:
        yield fp.PartialResponse(text="Alright, what else would you like to do?")
