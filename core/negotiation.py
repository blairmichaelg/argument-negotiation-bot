from typing import AsyncIterable
import fastapi_poe as fp
from utils.prompt_engineering import create_prompt


async def handle_negotiation(
    request: fp.QueryRequest, user_input: str, user_data: dict
) -> AsyncIterable[fp.PartialResponse]:
    """Handles user requests for generating negotiation scenarios."""

    scenario = user_input.replace("negotiation", "").strip()
    prompt = create_prompt("negotiation", topic=scenario)

    # Generate negotiation scenario
    async for msg in fp.stream_request(request, "GPT-4"):
        yield fp.PartialResponse(text=msg.text)

    yield fp.PartialResponse(text="\n\nWhat's your opening offer or position?")

    # Handle user's opening offer
    user_offer = request.query[-1].content

    # Analyze the offer and provide feedback
    analysis_prompt = (
        f"Analyze this opening offer in the context of the negotiation: {user_offer}"
    )
    async for msg in analyze_offer(request, analysis_prompt):
        yield msg

    yield fp.PartialResponse(
        text="\n\nWould you like to: \n"
        "1. Continue the negotiation?\n"
        "2. Receive advice on negotiation tactics?\n"
        "3. Do something else?"
    )

    # Handle user choice
    user_choice = request.query[-1].content
    if "1" in user_choice or "continue" in user_choice.lower():
        yield fp.PartialResponse(text="Okay, what's your next move or counter-offer?")
        # Handle continued negotiation - manage negotiation state
        async for msg in continue_negotiation(request, scenario, user_offer):
            yield msg
    elif "2" in user_choice or "advice" in user_choice.lower():
        async for msg in provide_negotiation_tactics(request, scenario):
            yield msg
    else:
        yield fp.PartialResponse(text="Alright, what else would you like to do?")
        # Handle other functionalities or end the interaction


async def analyze_offer(
    request: fp.QueryRequest, analysis_prompt: str
) -> AsyncIterable[fp.PartialResponse]:
    try:
        async for msg in fp.stream_request(request, "GPT-3.5-Turbo"):
            yield fp.PartialResponse(text=msg.text)
    except Exception as e:
        yield fp.PartialResponse(text=f"Error analyzing offer: {str(e)}")


async def provide_negotiation_tactics(
    request: fp.QueryRequest, scenario: str
) -> AsyncIterable[fp.PartialResponse]:
    prompt = f"Provide advanced negotiation tactics and strategies for the following scenario: {scenario}"
    try:
        async for msg in fp.stream_request(request, "Claude-instant"):
            yield fp.PartialResponse(text=msg.text)
    except Exception as e:
        yield fp.PartialResponse(text=f"Error providing negotiation tactics: {str(e)}")


async def continue_negotiation(
    request: fp.QueryRequest, scenario: str, user_offer: str
) -> AsyncIterable[fp.PartialResponse]:
    """Handles continued negotiation based on user's offer and scenario."""
    prompt = create_prompt(
        "continue_negotiation", topic=scenario, user_offer=user_offer
    )
    try:
        async for msg in fp.stream_request(request, "GPT-4"):
            yield fp.PartialResponse(text=msg.text)
    except Exception as e:
        yield fp.PartialResponse(text=f"Error continuing negotiation: {str(e)}")
