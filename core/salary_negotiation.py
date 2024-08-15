from typing import AsyncIterable, Dict
import fastapi_poe as fp
from utils.prompt_engineering import create_prompt

async def handle_functionality(request: fp.QueryRequest, job_details: str) -> AsyncIterable[fp.PartialResponse]:
    prompt = create_prompt("salary_negotiation", job_details)
    
    yield fp.PartialResponse(text="Analyzing the job details and preparing negotiation advice...\n\n")
    
    # Initial advice
    async for msg in fp.stream_request(request, "GPT-4", request.access_key, prompt=prompt):
        yield fp.PartialResponse(text=msg.text)
    
    # Market research
    yield fp.PartialResponse(text="\n\nConducting market research...\n\n")
    market_data = await get_market_data(request, job_details)
    for category, data in market_data.items():
        yield fp.PartialResponse(text=f"{category}:\n{data}\n\n")
    
    # Negotiation strategies
    yield fp.PartialResponse(text="Recommended negotiation strategies:\n\n")
    strategies = await get_negotiation_strategies(request, job_details, market_data)
    yield fp.PartialResponse(text=strategies)
    
    yield fp.PartialResponse(text="\n\nWould you like to practice a negotiation scenario or get advice on specific negotiation points?")

async def get_market_data(request: fp.QueryRequest, job_details: str) -> Dict[str, str]:
    market_prompt = f"Provide market research data for the following job: {job_details}. Include average salary range, typical benefits, and industry trends."
    market_data = {}
    async for msg in fp.stream_request(request, "GPT-3.5-Turbo", request.access_key, prompt=market_prompt):
        # Parse the response to extract market data
        # This is a simplified version; in a real implementation, you'd parse the response more robustly
        sections = msg.text.split('\n\n')
        for section in sections:
            if ':' in section:
                key, value = section.split(':', 1)
                market_data[key.strip()] = value.strip()
    return market_data

async def get_negotiation_strategies(request: fp.QueryRequest, job_details: str, market_data: Dict[str, str]) -> str:
    strategy_prompt = f"Given the job details: {job_details}\n\nAnd the following market data:\n"
    for category, data in market_data.items():
        strategy_prompt += f"{category}: {data}\n"
    strategy_prompt += "\nProvide specific negotiation strategies and talking points."
    
    async for msg in fp.stream_request(request, "Claude-instant", request.access_key, prompt=strategy_prompt):
        return msg.text  # Return the first (and likely only) message as the strategies

async def process_functionality(job_details: str) -> str:
    return f"Preparing salary negotiation advice for: {job_details[:50]}..."  # Truncate for brevity

async def simulate_negotiation(request: fp.QueryRequest, job_details: str, user_proposal: str) -> AsyncIterable[fp.PartialResponse]:
    simulation_prompt = f"Simulate a salary negotiation for this job: {job_details}\n\nThe candidate has proposed: {user_proposal}\n\nProvide a realistic employer response and potential counter-offer."
    async for msg in fp.stream_request(request, "GPT-4", request.access_key, prompt=simulation_prompt):
        yield fp.PartialResponse(text=msg.text)