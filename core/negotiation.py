from typing import AsyncIterable
import fastapi_poe as fp
from utils.prompt_engineering import create_prompt

async def handle_negotiation(request: fp.QueryRequest, user_input: str, user_data: dict) -> AsyncIterable[fp.PartialResponse]:
    """Handles user requests for generating negotiation scenarios."""

    scenario = user_input.replace("negotiation", "").strip()
    prompt = create_prompt("negotiation", topic=scenario)

    # Generate negotiation scenario
    async for msg in fp.stream_request(request, "GPT-4", prompt=prompt):
        yield fp.PartialResponse(text=msg.text)

    yield fp.PartialResponse(text="\n\nWhat's your opening offer or position?")

    # Handle user's opening offer
    user_offer = await request.get_next_message()

    # Analyze the offer and provide feedback
    analysis_prompt = f"Analyze this opening offer in the context of the negotiation: {user_offer.content}"
    async for msg in fp.stream_request(request, "GPT-3.5-Turbo", prompt=analysis_prompt):
        yield fp.PartialResponse(text=msg.text)

    yield fp.PartialResponse(
        text="\n\nWould you like to: \n"
        "1. Continue the negotiation?\n"
        "2. Receive advice on negotiation tactics?\n"
        "3. Do something else?"
    )

    # Handle user choice
    user_choice = await request.get_next_message()
    if "1" in user_choice.content or "continue" in user_choice.content.lower():
        yield fp.PartialResponse(text="Okay, what's your next move or counter-offer?")
        # ... (Handle continued negotiation - you'll need to manage negotiation state)
    elif "2" in user_choice.content or "advice" in user_choice.content.lower():
        async for msg in await provide_negotiation_tactics(request, scenario):
            yield msg
    else:
        yield fp.PartialResponse(text="Alright, what else would you like to do?")
        # ... (Handle other functionalities or end the interaction)

async def provide_negotiation_tactics(request: fp.QueryRequest, scenario: str) -> AsyncIterable[fp.PartialResponse]:
    prompt = f"Provide advanced negotiation tactics and strategies for the following scenario: {scenario}"
    async for msg in fp.stream_request(request, "Claude-instant", prompt=prompt):
        yield fp.PartialResponse(text=msg.text)