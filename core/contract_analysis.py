from typing import AsyncIterable, Dict
import fastapi_poe as fp
from utils.prompt_engineering import create_prompt

async def handle_contract_analysis(request: fp.QueryRequest, user_input: str, user_data: dict) -> AsyncIterable[fp.PartialResponse]:
    """Handles user requests for contract analysis."""

    clause = user_input.replace("contract", "").strip()
    prompt = create_prompt("contract_analysis", topic=clause)

    yield fp.PartialResponse(text="Analyzing the contract clause...\n\n")

    # Initial analysis
    async for msg in fp.stream_request(request, "GPT-4", prompt=prompt):
        yield fp.PartialResponse(text=msg.text)

    # Detailed breakdown
    yield fp.PartialResponse(text="\n\nProviding a detailed breakdown:\n\n")
    breakdown = await get_detailed_breakdown(request, clause)
    for section, analysis in breakdown.items():
        yield fp.PartialResponse(text=f"{section}:\n{analysis}\n\n")

    # Legal implications
    yield fp.PartialResponse(text="Potential legal implications:\n\n")
    legal_analysis = await get_legal_implications(request, clause)
    yield fp.PartialResponse(text=legal_analysis)

    yield fp.PartialResponse(
        text="\n\nWould you like to: \n"
        "1. Suggest improvements to the clause?\n"
        "2. Analyze another clause?\n"
        "3. Do something else?"
    )

    # Handle user choice
    user_choice = await request.get_next_message()
    if "1" in user_choice.content or "suggest" in user_choice.content.lower():
        async for msg in await suggest_improvements(request, clause):
            yield msg
    elif "2" in user_choice.content or "analyze" in user_choice.content.lower():
        yield fp.PartialResponse(text="Okay, please provide the new contract clause.")
        # ... (Handle the new clause analysis - you can re-use this function)
    else:
        yield fp.PartialResponse(text="Alright, what else would you like to do?")
        # ... (Handle other functionalities or end the interaction)

async def get_detailed_breakdown(request: fp.QueryRequest, contract_clause: str) -> Dict[str, str]:
    breakdown_prompt = f"Provide a detailed breakdown of the following contract clause, including key terms, obligations, and potential risks:\n\n{contract_clause}"
    breakdown = {}
    async for msg in fp.stream_request(request, "GPT-4", prompt=breakdown_prompt):
        # Parse the response to extract breakdown sections
        sections = msg.text.split('\n\n')
        for section in sections:
            if ':' in section:
                key, value = section.split(':', 1)
                breakdown[key.strip()] = value.strip()
    return breakdown

async def get_legal_implications(request: fp.QueryRequest, contract_clause: str) -> str:
    legal_prompt = f"Analyze the potential legal implications and risks of the following contract clause:\n\n{contract_clause}"
    legal_analysis = ""
    async for msg in fp.stream_request(request, "Claude-instant", prompt=legal_prompt):
        legal_analysis += msg.text
    return legal_analysis

async def suggest_improvements(request: fp.QueryRequest, contract_clause: str) -> AsyncIterable[fp.PartialResponse]:
    improvement_prompt = f"Suggest improvements or alternative phrasings for the following contract clause to make it more favorable or clearer:\n\n{contract_clause}"
    async for msg in fp.stream_request(request, "GPT-4", prompt=improvement_prompt):
        yield fp.PartialResponse(text=msg.text)