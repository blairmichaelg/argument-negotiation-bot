from typing import AsyncIterable, Dict
import fastapi_poe as fp
from utils.prompt_engineering import create_prompt

async def handle_functionality(request: fp.QueryRequest, statement: str) -> AsyncIterable[fp.PartialResponse]:
    prompt = create_prompt("fact_check", statement)
    
    # Initial fact check
    yield fp.PartialResponse(text="Analyzing the statement...\n\n")
    async for msg in fp.stream_request(request, "GPT-3.5-Turbo", request.access_key, prompt=prompt):
        yield fp.PartialResponse(text=msg.text)
    
    # Detailed research
    yield fp.PartialResponse(text="\n\nConducting detailed research...\n\n")
    research_results = await conduct_research(request, statement)
    
    # Final verdict
    yield fp.PartialResponse(text="\n\nFinal verdict:\n\n")
    verdict = await get_final_verdict(request, statement, research_results)
    yield fp.PartialResponse(text=verdict)
    
    yield fp.PartialResponse(text="\n\nWould you like to explore the sources or check another statement?")

async def conduct_research(request: fp.QueryRequest, statement: str) -> Dict[str, str]:
    research_prompt = f"Provide credible sources and additional context for the statement: {statement}"
    sources = {}
    async for msg in fp.stream_request(request, "Claude-instant", request.access_key, prompt=research_prompt):
        # Parse the response to extract sources
        # This is a simplified version; in a real implementation, you'd parse the response more robustly
        sources[f"Source {len(sources) + 1}"] = msg.text
        if len(sources) >= 3:  # Limit to 3 sources for brevity
            break
    return sources

async def get_final_verdict(request: fp.QueryRequest, statement: str, research_results: Dict[str, str]) -> str:
    verdict_prompt = f"Given the statement '{statement}' and the following research:\n"
    for source, info in research_results.items():
        verdict_prompt += f"{source}: {info}\n"
    verdict_prompt += "\nProvide a final fact-check verdict."
    
    async for msg in fp.stream_request(request, "GPT-4", request.access_key, prompt=verdict_prompt):
        return msg.text  # Return the first (and likely only) message as the verdict

async def process_functionality(statement: str) -> str:
    return f"Fact-checking statement: {statement}"

async def suggest_related_facts(request: fp.QueryRequest, statement: str) -> AsyncIterable[fp.PartialResponse]:
    prompt = f"Suggest related facts or context for further exploration based on this statement: {statement}"
    async for msg in fp.stream_request(request, "GPT-3.5-Turbo", request.access_key, prompt=prompt):
        yield fp.PartialResponse(text=msg.text)