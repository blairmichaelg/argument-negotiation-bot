from typing import AsyncIterable
import fastapi_poe as fp
from fastapi_poe import BotError, PartialResponse, QueryRequest
import logging
from utils.prompt_engineering import create_prompt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def fact_check(
    statement: str, request: QueryRequest
) -> AsyncIterable[PartialResponse]:
    """
    Suggest related facts or context for further exploration based on this statement.
    """
    request.query.append(
        fp.ProtocolMessage(
            content=create_prompt("fact-check", topic=statement), role="user"
        )
    )
    async for msg in fp.stream_request(request, "GPT-3.5-Turbo", request.access_key):
        yield PartialResponse(text=msg.text)


async def handle_fact_check(
    request: fp.QueryRequest, user_input: str
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

    yield fp.PartialResponse(
        text="\n\nWould you like to:\n"
        "1. Explore additional sources?\n"
        "2. Fact-check another statement?\n"
        "3. Do something else?"
    )

    # Handle user choice for further actions
    user_choice = request.query[-1].content.lower()
    if "1" in user_choice or "explore" in user_choice:
        yield fp.PartialResponse(
            text="Okay, here are some additional sources to consider.\n\n"
        )
        request.query.append(
            fp.ProtocolMessage(
                content=create_prompt("fact-check", topic=statement), role="user"
            )
        )
        async for msg in fp.stream_request(request, "GPT-4", request.access_key):
            yield fp.PartialResponse(text=msg.text)
    elif "2" in user_choice or "fact-check" in user_choice:
        yield fp.PartialResponse(text="Okay, please provide the new statement.")
    else:
        yield fp.PartialResponse(text="Alright, what else would you like to do?")
