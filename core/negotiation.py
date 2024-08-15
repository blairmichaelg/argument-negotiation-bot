from typing import AsyncIterable
import fastapi_poe as fp
from utils.prompt_engineering import create_prompt

async def handle_functionality(request: fp.QueryRequest, scenario: str) -> AsyncIterable[fp.PartialResponse]:
    prompt = create_prompt("negotiation", scenario)
    
    # Generate negotiation scenario
    async for msg in fp.stream_request(request, "GPT-4", request.access_key):
        yield fp.PartialResponse(text=msg.text)
    
    yield fp.PartialResponse(text="\n\nWhat's your opening offer or position?")
    
    # Wait for user's opening offer
    user_offer = await get_user_offer(request)
    
    # Analyze the offer and provide feedback
    analysis_prompt = f"Analyze this opening offer in the context of the negotiation: {user_offer}"
    async for msg in fp.stream_request(request, "GPT-3.5-Turbo", request.access_key, prompt=analysis_prompt):
        yield fp.PartialResponse(text=msg.text)
    
    yield fp.PartialResponse(text="\n\nWould you like to continue the negotiation or receive advice on negotiation tactics?")

async def get_user_offer(request: fp.QueryRequest) -> str:
    # This function would wait for the user's response in a real implementation
    # For now, we'll just return a default offer
    return "I propose a 10% increase in salary."

async def process_functionality(scenario: str) -> str:
    # This function can be used for any preprocessing or additional logic
    return f"Negotiation scenario: {scenario}"

async def generate_counter_offer(request: fp.QueryRequest, scenario: str, last_offer: str) -> AsyncIterable[fp.PartialResponse]:
    prompt = f"Given the scenario: {scenario}, and the last offer: {last_offer}, generate a reasonable counter-offer."
    async for msg in fp.stream_request(request, "GPT-4", request.access_key, prompt=prompt):
        yield fp.PartialResponse(text=msg.text)

async def provide_negotiation_tactics(request: fp.QueryRequest, scenario: str) -> AsyncIterable[fp.PartialResponse]:
    prompt = f"Provide advanced negotiation tactics and strategies for the following scenario: {scenario}"
    async for msg in fp.stream_request(request, "Claude-instant", request.access_key, prompt=prompt):
        yield fp.PartialResponse(text=msg.text)

async def evaluate_negotiation_outcome(request: fp.QueryRequest, scenario: str, final_agreement: str) -> AsyncIterable[fp.PartialResponse]:
    prompt = f"Evaluate the outcome of this negotiation. Scenario: {scenario}. Final agreement: {final_agreement}"
    async for msg in fp.stream_request(request, "GPT-4", request.access_key, prompt=prompt):
        yield fp.PartialResponse(text=msg.text)