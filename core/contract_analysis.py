from typing import AsyncIterable, Dict
import fastapi_poe as fp
from utils.prompt_engineering import create_prompt
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def handle_contract_analysis(
    request: fp.QueryRequest, user_input: str, user_data: dict
) -> AsyncIterable[fp.PartialResponse]:
    """
    Handles user requests for contract analysis.

    Parameters:
        request (fp.QueryRequest): The request object containing user input and context.
        user_input (str): The user's input indicating the contract clause to analyze.
        user_data (dict): User-specific data for personalized responses.

    Yields:
        AsyncIterable[fp.PartialResponse]: Responses to the user regarding contract analysis.
    """
    clause = user_input.replace("contract", "").strip()
    prompt = create_prompt("contract_analysis", topic=clause)

    yield fp.PartialResponse(text="Analyzing the contract clause...\n\n")
    logger.info("Starting contract clause analysis")

    try:
        # Perform initial analysis of the contract clause
        async for msg in fp.stream_request(request, "GPT-4"):
            yield fp.PartialResponse(text=msg.text)  # Accessing the 'text' attribute

        # Provide a detailed breakdown of the clause
        yield fp.PartialResponse(text="\n\nProviding a detailed breakdown:\n\n")
        breakdown = await get_detailed_breakdown(request, clause)
        for section, analysis in breakdown.items():
            yield fp.PartialResponse(text=f"{section}:\n{analysis}\n\n")

        # Analyze potential legal implications of the clause
        yield fp.PartialResponse(text="Potential legal implications:\n\n")
        legal_analysis = await get_legal_implications(request, clause)
        yield fp.PartialResponse(text=legal_analysis)

        # Provide sentiment analysis of the clause
        yield fp.PartialResponse(text="Sentiment analysis of the clause:\n\n")
        sentiment = await get_sentiment_analysis(request, clause)
        yield fp.PartialResponse(text=sentiment)

        yield fp.PartialResponse(
            text="\n\nWould you like to: \n"
            "1. Suggest improvements to the clause?\n"
            "2. Analyze another clause?\n"
            "3. Do something else?"
        )

        # Handle user choice for further actions
        user_choice = json.loads(request.json())
        if any("1" in msg or "suggest" in msg.lower() for msg in user_choice):
            async for msg in suggest_improvements(request, clause):
                yield msg
        elif any("2" in msg or "analyze" in msg.lower() for msg in user_choice):
            yield fp.PartialResponse(
                text="Okay, please provide the new contract clause."
            )
        else:
            yield fp.PartialResponse(text="Alright, what else would you like to do?")
    except Exception as e:
        logger.error(f"Error during contract analysis: {e}")
        yield fp.PartialResponse(
            text="An error occurred during the analysis. Please try again later."
        )


async def get_detailed_breakdown(
    request: fp.QueryRequest, contract_clause: str
) -> Dict[str, str]:
    """
    Provides a detailed breakdown of a contract clause.

    Parameters:
        request (fp.QueryRequest): The request object.
        contract_clause (str): The contract clause to analyze.

    Returns:
        Dict[str, str]: A dictionary containing section titles and their corresponding analyses.
    """
    breakdown_prompt = f"Provide a detailed breakdown of the following contract clause, including key terms, obligations, and potential risks:\n\n{contract_clause}"
    breakdown = {}
    try:
        async for msg in fp.stream_request(request, "GPT-4"):
            sections = msg.text.split('\n\n')  # Accessing the 'text' attribute
            for section in sections:
                if ':' in section:
                    key, value = section.split(':', 1)
                    breakdown[key.strip()] = value.strip()
    except Exception as e:
        logger.error(f"Error during detailed breakdown: {e}")
    return breakdown


async def get_legal_implications(request: fp.QueryRequest, contract_clause: str) -> str:
    """
    Analyzes the potential legal implications of a contract clause.

    Parameters:
        request (fp.QueryRequest): The request object.
        contract_clause (str): The contract clause to analyze.

    Returns:
        str: A summary of potential legal risks and implications.
    """
    legal_prompt = f"Analyze the potential legal implications and risks of the following contract clause:\n\n{contract_clause}"
    legal_analysis = ""
    try:
        async for msg in fp.stream_request(request, "Claude-instant"):
            legal_analysis += msg.text  # Accessing the 'text' attribute
    except Exception as e:
        logger.error(f"Error during legal implications analysis: {e}")
    return legal_analysis


async def suggest_improvements(
    request: fp.QueryRequest, contract_clause: str
) -> AsyncIterable[fp.PartialResponse]:
    """
    Suggests improvements or alternative phrasings for a contract clause.

    Parameters:
        request (fp.QueryRequest): The request object.
        contract_clause (str): The contract clause to improve.

    Yields:
        AsyncIterable[fp.PartialResponse]: Suggested improvements for the clause.
    """
    improvement_prompt = f"Suggest improvements or alternative phrasings for the following contract clause to make it more favorable or clearer:\n\n{contract_clause}"
    try:
        async for msg in fp.stream_request(request, "GPT-4"):
            yield fp.PartialResponse(text=msg.text)  # Accessing the 'text' attribute
    except Exception as e:
        logger.error(f"Error during suggestions for improvements: {e}")


async def get_sentiment_analysis(request: fp.QueryRequest, contract_clause: str) -> str:
    """
    Provides a sentiment analysis of a contract clause.

    Parameters:
        request (fp.QueryRequest): The request object.
        contract_clause (str): The contract clause to analyze.

    Returns:
        str: A sentiment analysis of the contract clause.
    """
    sentiment_prompt = f"Provide a sentiment analysis of the following contract clause:\n\n{contract_clause}"
    sentiment_analysis = ""
    try:
        async for msg in fp.stream_request(request, "GPT-4"):
            sentiment_analysis += msg.text  # Accessing the 'text' attribute
    except Exception as e:
        logger.error(f"Error during sentiment analysis: {e}")
    return sentiment_analysis
