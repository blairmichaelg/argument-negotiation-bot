from typing import AsyncIterable
import fastapi_poe as fp
from utils.prompt_engineering import create_prompt


async def handle_debate(
    request: fp.QueryRequest, user_input: str, user_data: dict
) -> AsyncIterable[fp.PartialResponse]:
    """
    Handles user requests for generating debates.

    Parameters:
        request (fp.QueryRequest): The request object containing user input and context.
        user_input (str): The user's input indicating the debate topic.
        user_data (dict): User-specific data for personalized responses.

    Yields:
        AsyncIterable[fp.PartialResponse]: Responses to the user regarding the debate.
    """
    topic = user_input.replace("debate", "").strip()  # Extract the topic
    prompt = create_prompt("debate", topic=topic)

    async for msg in fp.stream_request(request, "GPT-3.5-Turbo", prompt=prompt):
        yield fp.PartialResponse(text=msg.text)

    yield fp.PartialResponse(text="\n\nWhich side would you like to argue for?")

    # Handle user's side choice
    user_choice = await request.get_next_message()
    chosen_side = user_choice.content.lower()

    # Generate arguments for the chosen side
    argument_prompt = f"Generate strong arguments for the {chosen_side} side of the debate on: {topic}"
    async for msg in fp.stream_request(request, "GPT-4", prompt=argument_prompt):
        yield fp.PartialResponse(text=msg.text)

    yield fp.PartialResponse(
        text="\n\nWould you like to:\n"
        "1. Continue the debate?\n"
        "2. Explore counterarguments?\n"
        "3. Do something else?"
    )

    # Handle further debate actions
    next_action = await request.get_next_message()
    if "1" in next_action.content or "continue" in next_action.content.lower():
        yield fp.PartialResponse(text="Okay, let's continue. What's your next point?")
    elif "2" in next_action.content or "counter" in next_action.content.lower():
        async for msg in await generate_counterarguments(request, topic, chosen_side):
            yield msg
    else:
        yield fp.PartialResponse(text="Alright, what else would you like to do?")


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
    prompt = f"Generate strong counterarguments against the {side} side of the debate on: {topic}"
    async for msg in fp.stream_request(request, "GPT-4", prompt=prompt):
        yield fp.PartialResponse(text=msg.text)
