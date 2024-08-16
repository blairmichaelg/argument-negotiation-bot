from typing import AsyncIterable, Dict
import fastapi_poe as fp
from utils.prompt_engineering import create_prompt


async def handle_fact_check(
    request: fp.QueryRequest, user_input: str, user_data: dict
) -> AsyncIterable[fp.PartialResponse]:
    """
    Handles user requests for fact-checking statements.

    Parameters:
        request (fp.QueryRequest): The request object containing user input and context.
        user_input (str): The user's input statement to be fact-checked.
        user_data (dict): User-specific data for personalized responses.

    Yields:
        AsyncIterable[fp.PartialResponse]: Responses regarding the fact-checking process.
    """
    statement = user_input.replace("fact-check", "").strip()
    prompt = create_prompt("fact_check", topic=statement)

    # Initial fact check
    yield fp.PartialResponse(text="Analyzing the statement...\n\n")
    async for msg in fp.stream_request(request, "GPT-3.5-Turbo", prompt=prompt):
        yield fp.PartialResponse(text=msg.text)

    # Detailed research
    yield fp.PartialResponse(text="\n\nConducting detailed research...\n\n")
    research_results = await conduct_research(request, statement)
    for source, info in research_results.items():
        yield fp.PartialResponse(text=f"{source}: {info}\n\n")

    # Final verdict
    yield fp.PartialResponse(text="\n\nFinal verdict:\n\n")
    verdict = await get_final_verdict(request, statement, research_results)
    yield fp.PartialResponse(text=verdict)

    yield fp.PartialResponse(
        text="\n\nWould you like to: \n"
        "1. Explore related facts?\n"
        "2. Check another statement?\n"
        "3. Do something else?"
    )

    # Handle user choice
    user_choice = await request.get_next_message()
    if "1" in user_choice.content or "related" in user_choice.content.lower():
        async for msg in await suggest_related_facts(request, statement):
            yield msg
    elif "2" in user_choice.content or "check" in user_choice.content.lower():
        yield fp.PartialResponse(text="Okay, please provide the new statement.")
    else:
        yield fp.PartialResponse(text="Alright, what else would you like to do?")


async def conduct_research(request: fp.QueryRequest, statement: str) -> Dict[str, str]:
    """
    Conducts research to find credible sources related to the statement.

    Parameters:
        request (fp.QueryRequest): The request object.
        statement (str): The statement to research.

    Returns:
        Dict[str, str]: A dictionary of sources and their corresponding information.
    """
    research_prompt = f"Provide credible sources and additional context for the statement: {statement}"
    sources = {}
    async for msg in fp.stream_request(
        request, "Claude-instant", prompt=research_prompt
    ):
        # Parse the response to extract sources
        sections = msg.text.split('\n\n')
        for section in sections:
            if ':' in section:
                key, value = section.split(':', 1)
                sources[key.strip()] = value.strip()
        if len(sources) >= 3:  # Limit to 3 sources for brevity
            break
    return sources


async def get_final_verdict(
    request: fp.QueryRequest, statement: str, research_results: Dict[str, str]
) -> str:
    """
    Provides a final verdict based on the statement and research results.

    Parameters:
        request (fp.QueryRequest): The request object.
        statement (str): The statement being fact-checked.
        research_results (Dict[str, str]): The results from the research.

    Returns:
        str: The final fact-check verdict.
    """
    verdict_prompt = f"Given the statement '{statement}' and the following research:\n"
    for source, info in research_results.items():
        verdict_prompt += f"{source}: {info}\n"
    verdict_prompt += "\nProvide a final fact-check verdict."

    verdict = ""
    async for msg in fp.stream_request(request, "GPT-4", prompt=verdict_prompt):
        verdict += msg.text
    return verdict


async def suggest_related_facts(
    request: fp.QueryRequest, statement: str
) -> AsyncIterable[fp.PartialResponse]:
    """
    Suggests related facts or context for further exploration based on the statement.

    Parameters:
        request (fp.QueryRequest): The request object.
        statement (str): The statement for which to suggest related facts.

    Yields:
        AsyncIterable[fp.PartialResponse]: Suggested related facts.
    """
    prompt = f"Suggest related facts or context for further exploration based on this statement: {statement}"
    async for msg in fp.stream_request(request, "GPT-3.5-Turbo", prompt=prompt):
        yield fp.PartialResponse(text=msg.text)
