from typing import AsyncIterable
import fastapi_poe as fp
from utils.prompt_engineering import create_prompt
from fastapi_poe.client import BotError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def handle_debate(
    request: fp.QueryRequest, user_input: str
) -> AsyncIterable[fp.PartialResponse]:
    """
    Handles user requests for generating debates.

    Parameters:
        request (fp.QueryRequest): The request object containing user input and context.
        user_input (str): The user's input indicating the debate topic.

    Yields:
        AsyncIterable[fp.PartialResponse]: Responses to the user regarding the debate.
    """
    topic = user_input.replace("debate", "").strip()  # Extract the topic
    if not topic:
        raise BotError("Please provide a debate topic.")

    request.query.append(
        fp.ProtocolMessage(content=create_prompt("debate", topic=topic), role="user")
    )

    async for msg in fp.stream_request(request, "GPT-4", request.access_key):
        yield msg  # Send the generated response to the user for the debate topic prompt

    yield fp.PartialResponse(
        text="\n\nWhich side would you like to argue for?\n" "1. For\n" "2. Against"
    )  # Ask the user to choose a side for the debate topic

    user_choice = request.query[-1].content.lower()
    chosen_side = user_choice
    if "1" in user_choice or "for" in user_choice:
        chosen_side = "for"
    elif "2" in user_choice or "against" in user_choice:
        chosen_side = "against"
    else:
        yield fp.PartialResponse(
            text="I'm sorry, I didn't understand your choice. Please try again."
        )
        return

    request.query.append(
        fp.ProtocolMessage(
            content=create_prompt(
                "debate", topic=f"Generate an argument {chosen_side} the topic: {topic}"
            ),
            role="user",
        )
    )
    async for msg in fp.stream_request(request, "GPT-4", request.access_key):
        yield fp.PartialResponse(text=msg.text)

    yield fp.PartialResponse(
        text="\n\nWould you like to:\n"
        "1. Continue the debate?\n"
        "2. Explore counterarguments?\n"
        "3. Do something else?"
    )

    next_action = request.query[-1].content.lower()
    if "1" in next_action or "continue" in next_action:
        yield fp.PartialResponse(text="Okay, let's continue. What's your next point?")
    elif "2" in next_action or "counter" in next_action:
        async for msg in generate_counterarguments(request, topic, chosen_side):
            yield msg
    else:
        yield fp.PartialResponse(text="Alright, what else would you like to do?")
        return


async def generate_counterarguments(
    request: fp.QueryRequest, topic: str, side: str
) -> AsyncIterable[fp.PartialResponse]:
    """
    Generates strong counterarguments against a specified side of the debate.

    Parameters:
        request (fp.QueryRequest): The request object.
        topic (str): The debate topic.
        side (str): The side against which to generate counterarguments.

    Yields:
        AsyncIterable[fp.PartialResponse]: Counterarguments against the specified side.
    """
    request.query.append(
        fp.ProtocolMessage(
            content=f"Generate strong counterarguments against the following argument: {side} the topic: {topic}",
            role="user",
        )
    )
    async for msg in fp.stream_request(request, "GPT-4", request.access_key):
        yield fp.PartialResponse(text=msg.text)
