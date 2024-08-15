from typing import AsyncIterable
import fastapi_poe as fp
from utils.prompt_engineering import create_prompt

async def handle_functionality(request: fp.QueryRequest, topic: str) -> AsyncIterable[fp.PartialResponse]:
    prompt = create_prompt("debate", topic)
    
    # Generate opposing viewpoints
    async for msg in fp.stream_request(request, "GPT-3.5-Turbo", request.access_key):
        yield fp.PartialResponse(text=msg.text)
    
    yield fp.PartialResponse(text="\n\nWhich side would you like to argue for?")
    
    # Wait for user's choice
    user_choice = await get_user_choice(request)
    
    # Generate arguments for the chosen side
    argument_prompt = f"Generate strong arguments for the {user_choice} side of the debate on: {topic}"
    async for msg in fp.stream_request(request, "GPT-4", request.access_key, prompt=argument_prompt):
        yield fp.PartialResponse(text=msg.text)
    
    yield fp.PartialResponse(text="\n\nWould you like to continue the debate or explore counterarguments?")

async def get_user_choice(request: fp.QueryRequest) -> str:
    # This function would wait for the user's response in a real implementation
    # For now, we'll just return a default choice
    return "pro"

async def process_functionality(topic: str) -> str:
    # This function can be used for any preprocessing or additional logic
    return f"Debate topic: {topic}"

async def generate_counterarguments(request: fp.QueryRequest, topic: str, side: str) -> AsyncIterable[fp.PartialResponse]:
    prompt = f"Generate strong counterarguments against the {side} side of the debate on: {topic}"
    async for msg in fp.stream_request(request, "GPT-4", request.access_key, prompt=prompt):
        yield fp.PartialResponse(text=msg.text)

async def evaluate_argument(request: fp.QueryRequest, argument: str) -> AsyncIterable[fp.PartialResponse]:
    prompt = f"Evaluate the strength and weaknesses of this argument: {argument}"
    async for msg in fp.stream_request(request, "Claude-instant", request.access_key, prompt=prompt):
        yield fp.PartialResponse(text=msg.text)