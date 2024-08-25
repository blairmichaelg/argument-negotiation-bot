import fastapi_poe as fp
from typing import AsyncIterable
from utils.prompt_engineering import create_prompt
from fastapi_poe.client import BotError
from utils.helpers import analyze_sentiment
from utils.database import (
    NegotiationScenario,
    get_db,
    create_negotiation_scenario,
    get_negotiation_scenario_by_id,
    update_negotiation_scenario,
)
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def handle_negotiation(
    request: fp.QueryRequest, user_input: str
) -> AsyncIterable[fp.PartialResponse]:
    """Handles user requests for generating negotiation scenarios."""

    scenario = user_input.replace("negotiation", "").strip()
    if not scenario:
        raise BotError("Please provide a negotiation scenario.")

    db = await get_db().__anext__()
    scenario_id = int(scenario)
    negotiation_scenario = await get_negotiation_scenario_by_id(db, int(scenario_id))
    if not negotiation_scenario:
        negotiation_scenario = await create_negotiation_scenario(db, scenario)

    # Generate negotiation scenario
    request.query.append(
        fp.ProtocolMessage(
            content=create_prompt("negotiation", topic=scenario), role="user"
        )
    )
    async for msg in fp.stream_request(
        request,
        "GPT-4",
        request.access_key,
    ):
        yield fp.PartialResponse(text=msg.text)

    yield fp.PartialResponse(text="\n\nWhat's your opening offer or position?")

    # Handle user's opening offer or position and continue the negotiation.
    user_offer = request.query[-1].content
    db = await get_db().__anext__()

    # Analyze the offer and provide feedback
    analysis_prompt = (
        f"Analyze this opening offer in the context of the negotiation: {user_offer}"
        f"\n\nPrevious offers: {negotiation_scenario.user_offers}"
        f"\n\nPrevious bot responses: {negotiation_scenario.bot_responses}"
    )

    async for msg in analyze_offer(
        request,
        analysis_prompt=analysis_prompt,
        scenario=scenario,
        user_offer=user_offer,
    ):
        yield msg

    # Generate bot response based on user offer and previous interactions
    bot_response = await generate_bot_response(
        request, scenario, user_offer, negotiation_scenario
    )
    db = await get_db().__anext__()
    negotiation_scenario = await get_negotiation_scenario_by_id(
        db, negotiation_scenario.id.value
    )
    if negotiation_scenario:
        negotiation_scenario.user_offers.append(user_offer)
        negotiation_scenario.bot_responses.append(bot_response)
        await update_negotiation_scenario(
            db,
            negotiation_scenario.id,
            negotiation_scenario.user_offers,
            negotiation_scenario.bot_responses,
        )

    yield fp.PartialResponse(text=f"\n\n{bot_response}")

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
    request: fp.QueryRequest, analysis_prompt: str, scenario: str, user_offer: str
) -> AsyncIterable[fp.PartialResponse]:
    try:
        db = await get_db().__anext__()
        scenario_id = int(scenario)
        negotiation_scenario = await get_negotiation_scenario_by_id(db, scenario_id)
        if negotiation_scenario:
            request.query.append(
                fp.ProtocolMessage(
                    content=create_prompt(
                        "continue_negotiation",
                        topic=scenario,
                        user_offer=user_offer,
                        user_offers=negotiation_scenario.user_offers,
                        bot_responses=negotiation_scenario.bot_responses,
                    ),
                    role="user",
                )
            )
            async for msg in fp.stream_request(
                request,
                "GPT-4",
                request.access_key,
            ):
                yield fp.PartialResponse(text=msg.text)
            request.query.append(
                fp.ProtocolMessage(content=analysis_prompt, role="user")
            )
            async for msg in fp.stream_request(
                request, "GPT-3.5-Turbo", request.access_key
            ):
                yield fp.PartialResponse(text=msg.text)
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        yield fp.PartialResponse(text=f"Error analyzing offer: {str(e)}")


async def provide_negotiation_tactics(
    request: fp.QueryRequest, scenario: str
) -> AsyncIterable[fp.PartialResponse]:
    prompt = f"Provide advanced negotiation tactics and strategies for the following scenario: {scenario}"
    try:
        request.query.append(fp.ProtocolMessage(content=prompt, role="user"))
        async for msg in fp.stream_request(
            request, "Claude-instant", request.access_key
        ):
            yield fp.PartialResponse(text=msg.text)
    except Exception as e:
        yield fp.PartialResponse(text=f"Error providing negotiation tactics: {str(e)}")


async def continue_negotiation(
    request: fp.QueryRequest, scenario: str, user_offer: str
) -> AsyncIterable[fp.PartialResponse]:
    """Handles continued negotiation based on user's offer and scenario."""

    try:
        db = await get_db().__anext__()
        negotiation_scenario = await get_negotiation_scenario_by_id(db, int(scenario))
        if negotiation_scenario:
            request.query.append(
                fp.ProtocolMessage(
                    content=create_prompt(
                        "continue_negotiation",
                        topic=scenario,
                        user_offer=user_offer,
                        user_offers=negotiation_scenario.user_offers,
                        bot_responses=negotiation_scenario.bot_responses,
                    ),
                    role="user",
                )
            )
            async for msg in fp.stream_request(
                request,
                "GPT-4",
                request.access_key,
            ):
                yield fp.PartialResponse(text=msg.text)
    except Exception as e:
        yield fp.PartialResponse(text=f"Error continuing negotiation: {str(e)}")


async def generate_bot_response(
    request: fp.QueryRequest,
    scenario: str,
    user_offer: str,
    negotiation_scenario: NegotiationScenario,
) -> str:
    """Generates a bot response based on the user's offer and negotiation state."""
    prompt = (
        f"You are negotiating in the following scenario: {scenario}\n\n"
        f"The user has made the following offer: {user_offer}\n\n"
        f"Previous offers: {negotiation_scenario.user_offers}\n\n"
        f"Previous bot responses: {negotiation_scenario.bot_responses}\n\n"
        f"Generate a realistic and strategic response to the user's offer."
    )
    try:
        request.query.append(fp.ProtocolMessage(content=prompt, role="user"))
        async for msg in fp.stream_request(request, "GPT-4", request.access_key):
            response = msg.text
            sentiment = analyze_sentiment(response)
            return f"{response}\n\n(Sentiment: {sentiment})"
    except Exception as e:
        logger.error(f"Error generating bot response: {str(e)}")
        return "I'm having trouble responding right now. Please try again later."

    # Ensure a return statement in case the loop does not execute
    return "No response generated."
