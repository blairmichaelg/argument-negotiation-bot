"""Error handling utilities for the Argument and Negotiation Master Bot."""

import logging
from typing import Union

import fastapi_poe as fp

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BotError(Exception):
    """Custom exception class for bot-specific errors."""
    pass

async def handle_error(e: Exception) -> Union[fp.ErrorResponse, fp.PartialResponse]:
    """
    Handle errors and return appropriate responses.

    Args:
        e (Exception): The exception that occurred.

    Returns:
        Union[fp.ErrorResponse, fp.PartialResponse]: An error response for the user.
    """
    if isinstance(e, BotError):
        logger.warning(f"Bot-specific error occurred: {str(e)}")
        return fp.PartialResponse(
            text=f"I encountered an issue: {str(e)}. Please try rephrasing your request."
        )
    elif isinstance(e, fp.PoeException):
        logger.error(f"Poe API error occurred: {str(e)}")
        return fp.ErrorResponse(
            text="An error occurred while communicating with the Poe API. Please try again later.",
            raw_response=str(e),
            allow_retry=True
        )
    else:
        logger.exception("An unexpected error occurred")
        return fp.ErrorResponse(
            text="An unexpected error occurred. Our team has been notified. Please try again later.",
            raw_response=str(e),
            allow_retry=False
        )

def validate_input(input_string: str, max_length: int = 1000) -> str:
    """
    Validate and sanitize user input.

    Args:
        input_string (str): The input string to validate.
        max_length (int, optional): Maximum allowed length of the input. Defaults to 1000.

    Returns:
        str: Sanitized input string.

    Raises:
        BotError: If the input is invalid or too long.
    """
    if not input_string.strip():
        raise BotError("Input cannot be empty.")
    if len(input_string) > max_length:
        raise BotError(f"Input exceeds maximum length of {max_length} characters.")
    return input_string.strip()