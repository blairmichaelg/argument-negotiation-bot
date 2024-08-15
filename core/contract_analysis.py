from typing import AsyncIterable, Dict
import fastapi_poe as fp
from utils.prompt_engineering import create_prompt

async def handle_functionality(request: fp.QueryRequest, contract_clause: str) -> AsyncIterable[fp.PartialResponse]:
    prompt = create_prompt("contract_analysis", contract_clause)
    
    yield fp.PartialResponse(text="Analyzing the contract clause...\n\n")
    
    # Initial analysis
    async for msg in fp.stream_request(request, "GPT-4", request.access_key, prompt=prompt):
        yield fp.PartialResponse(text=msg.text)
    
    # Detailed breakdown
    yield fp.PartialResponse(text="\n\nProviding a detailed breakdown:\n\n")
    breakdown = await get_detailed_breakdown(request, contract_clause)
    for section, analysis in breakdown.items():
        yield fp.PartialResponse(text=f"{section}:\n{analysis}\n\n")
    
    # Legal implications
    yield fp.PartialResponse(text="Potential legal implications:\n\n")
    legal_analysis = await get_legal_implications(request, contract_clause)
    yield fp.PartialResponse(text=legal_analysis)
    
    yield fp.PartialResponse(text="\n\nWould you like to suggest improvements or analyze another clause?")

async def get_detailed_breakdown(request: fp.QueryRequest, contract_clause: str) -> Dict[str, str]:
    breakdown_prompt = f"Provide a detailed breakdown of the following contract clause, including key terms, obligations, and potential risks:\n\n{contract_clause}"
    breakdown = {}
    async for msg in fp.stream_request(request, "GPT-4", request.access_key, prompt=breakdown_prompt):
        # Parse the response to extract breakdown sections
        # This is a simplified version; in a real implementation, you'd parse the response more robustly
        sections = msg.text.split('\n\n')
        for section in sections:
            if ':' in section:
                key, value = section.split(':', 1)
                breakdown[key.strip()] = value.strip()
    return breakdown

async def get_legal_implications(request: fp.QueryRequest, contract_clause: str) -> str:
    legal_prompt = f"Analyze the potential legal implications and risks of the following contract clause:\n\n{contract_clause}"
    async for msg in fp.stream_request(request, "Claude-instant", request.access_key, prompt=legal_prompt):
        return msg.text  # Return the first (and likely only) message as the legal analysis

async def process_functionality(contract_clause: str) -> str:
    return f"Analyzing contract clause: {contract_clause[:50]}..."  # Truncate for brevity

async def suggest_improvements(request: fp.QueryRequest, contract_clause: str) -> AsyncIterable[fp.PartialResponse]:
    improvement_prompt = f"Suggest improvements or alternative phrasings for the following contract clause to make it more favorable or clearer:\n\n{contract_clause}"
    async for msg in fp.stream_request(request, "GPT-4", request.access_key, prompt=improvement_prompt):
        yield fp.PartialResponse(text=msg.text)