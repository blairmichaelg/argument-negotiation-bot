""" The functions in this module leverage the OpenAI API to analyze contract clauses, identify potential legal implications, suggest improvements, and provide sentiment analysis. """

from typing import AsyncIterable, Dict
import fastapi_poe as fp
from utils.prompt_engineering import create_prompt
from utils.error_handling import BotError

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # Change to DEBUG for more detailed logs
logging.getLogger("transformers").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def handle_contract_analysis(
    request: fp.QueryRequest, user_input: str
) -> AsyncIterable[fp.PartialResponse]:
    """
    Handles user requests for contract analysis.

    Parameters:
        request (fp.QueryRequest): The request object containing user input and context.
        user_input (str): The user's input indicating the contract clause to analyze.

    Yields:
        AsyncIterable[fp.PartialResponse]: Responses to the user regarding contract analysis.
    """
    clause = user_input.replace("contract", "").strip()
    if not clause:
        raise BotError("Please provide a contract clause to analyze.")

    yield fp.PartialResponse(text="Analyzing the contract clause...\n\n")
    logger.info("Starting contract clause analysis")

    try:
        # Perform initial analysis of the contract clause
        request.query.append(
            fp.ProtocolMessage(
                content=create_prompt("contract_analysis", topic=clause), role="user"
            )
        )
        async for msg in fp.stream_request(request, "GPT-4", request.access_key):
            yield fp.PartialResponse(text=msg.text)

        # Provide a detailed breakdown of the clause
        yield fp.PartialResponse(text="\n\nProviding a detailed breakdown:\n\n")
        breakdown = await get_detailed_breakdown(request, clause)
        for section, analysis in breakdown.items():
            yield fp.PartialResponse(text=f"{section}: \n{analysis}\n\n")

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
        user_choice = request.query[-1].content.lower()
        if "1" in user_choice or "suggest" in user_choice:
            async for msg in suggest_improvements(request, clause):
                yield msg
        elif "2" in user_choice or "analyze" in user_choice:
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
    breakdown = {}
    try:
        request.query.append(
            fp.ProtocolMessage(
                content=create_prompt("contract_analysis", topic=contract_clause),
                role="user",
            )
        )
        async for msg in fp.stream_request(request, "GPT-4", request.access_key):
            sections = msg.text.split('\n\n')
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
    legal_analysis = ""
    try:
        request.query.append(
            fp.ProtocolMessage(
                content=create_prompt("contract_analysis", topic=contract_clause),
                role="user",
            )
        )
        async for msg in fp.stream_request(
            request,
            "Claude-instant",
            request.access_key,
        ):
            legal_analysis += msg.text
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

    try:
        request.query.append(
            fp.ProtocolMessage(
                content=create_prompt("contract_analysis", topic=contract_clause),
                role="user",
            )
        )
        async for msg in fp.stream_request(request, "GPT-4", request.access_key):
            yield fp.PartialResponse(text=msg.text)
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
    sentiment_analysis = ""
    try:
        request.query.append(
            fp.ProtocolMessage(
                content=create_prompt("contract_analysis", topic=contract_clause),
                role="user",
            )
        )
        async for msg in fp.stream_request(request, "GPT-4", request.access_key):
            sentiment_analysis += msg.text
    except Exception as e:
        logger.error(f"Error during sentiment analysis: {e}")
    return sentiment_analysis
