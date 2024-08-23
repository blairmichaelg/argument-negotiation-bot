import logging
from typing import Union

from fastapi_poe import ErrorResponse, PartialResponse
from fastapi_poe.client import BotError

# Configure logging for error handling
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def handle_error(e: Exception) -> Union[ErrorResponse, PartialResponse]:
    """
    Handles errors, providing appropriate user feedback and logging.

    Parameters:
        e (Exception): The exception that occurred.

    Returns:
        Union[ErrorResponse, PartialResponse]: An error response for the user.
    """
    if isinstance(e, BotError):
        logger.warning(f"BotError: {str(e)}")
        return PartialResponse(
            text=f"I encountered an issue: {str(e)}. Please try rephrasing."
        )
    elif isinstance(e, ValueError):
        logger.warning(f"ValueError: {str(e)}")
        return PartialResponse(
            text="I'm having trouble with that request. Please try again later."
        )
    elif isinstance(e, RuntimeError):
        logger.error(f"RuntimeError: {str(e)}")
        return ErrorResponse(
            text="An unexpected error occurred. Please try again later.",
            raw_response=str(e),
            allow_retry=False,
        )
    else:
        logger.exception("Unexpected Error:")
        return ErrorResponse(
            text="An unexpected error occurred. We've been notified. Please try again later.",
            raw_response=str(e),
            allow_retry=False,
        )


def validate_input(input_string: str, max_length: int = 1000) -> str:
    """
    Validates user input, ensuring it's not empty and within length limits.

    Parameters:
        input_string (str): The input string to validate.
        max_length (int): The maximum allowed length of the input.

    Returns:
        str: The validated and sanitized input string.

    Raises:
        BotError: If the input is invalid or too long.
    """
    input_string = input_string.strip()
    if not input_string:
        raise BotError("Input cannot be empty.")
    if len(input_string) > max_length:
        raise BotError(
            f"Input is too long. Please limit it to {max_length} characters."
        )
    return input_string
