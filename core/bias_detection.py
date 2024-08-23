from typing import AsyncIterable, List, Dict
import fastapi_poe as fp
from utils.prompt_engineering import create_prompt
import logging
from fastapi_poe.client import BotError

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of common cognitive biases
COMMON_BIASES = [
    "Confirmation Bias",
    "Anchoring Bias",
    "Availability Heuristic",
    "Framing Effect",
    "Dunning-Kruger Effect",
    "Bandwagon Effect",
    "Negativity Bias",
    "Sunk Cost Fallacy",
]

# Cache for detected biases to improve performance
bias_cache: Dict[str, List[str]] = {}


async def handle_bias_detection(
    request: fp.QueryRequest, user_input: str, user_data: dict
) -> AsyncIterable[fp.PartialResponse]:
    """
    Handles user requests for cognitive bias detection.

    Parameters:
        request (fp.QueryRequest): The request object containing user input and context.
        user_input (str): The user's input argument for analysis.
        user_data (dict): User-specific data for personalized responses.

    Yields:
        AsyncIterable[fp.PartialResponse]: Responses to the user regarding bias analysis.
    """
    try:
        argument = user_input.replace("cognitive bias", "").strip()
        if not argument:
            raise BotError("Please provide an argument to analyze.")

        yield fp.PartialResponse(
            text="Analyzing the argument for cognitive biases...\n\n"
        )

        # Initial bias detection
        async for msg in fp.stream_request(
            request, "GPT-4", create_prompt("bias_detection", topic=argument)
        ):
            yield fp.PartialResponse(text=msg.text)

        # Check cache first
        if argument in bias_cache:
            detected_biases = bias_cache[argument]
        else:
            detected_biases = await detect_specific_biases(request, argument)
            bias_cache[argument] = detected_biases

        yield fp.PartialResponse(text="\n\nDetailed bias analysis:\n\n")
        for bias in detected_biases:
            explanation = await explain_bias(request, bias, argument)
            yield fp.PartialResponse(text=f"{bias}: \n{explanation}\n\n")

        yield fp.PartialResponse(
            text="\n\nWould you like to: \n"
            "1. Explore strategies to mitigate these biases?\n"
            "2. Analyze another argument?\n"
            "3. Do something else?"
        )

        # Handle user choice through WebSocket or another method
        user_choice = await get_user_choice(
            request
        )  # Implement this function based on your framework
        if "1" in user_choice or "mitigate" in user_choice.lower():
            async for msg in suggest_debiasing_strategies(request, detected_biases):
                yield msg
        elif "2" in user_choice or "analyze" in user_choice.lower():
            yield fp.PartialResponse(text="Okay, please provide the new argument.")
        else:
            yield fp.PartialResponse(text="Alright, what else would you like to do?")
    except Exception as e:
        logger.error(f"Error in handle_bias_detection: {e}")
        yield fp.PartialResponse(
            text="An error occurred while processing your request. Please try again."
        )


async def detect_specific_biases(request: fp.QueryRequest, argument: str) -> List[str]:
    """
    Detects specific cognitive biases present in the given argument.

    Parameters:
        request (fp.QueryRequest): The request object.
        argument (str): The argument to analyze for biases.

    Returns:
        List[str]: A list of detected cognitive biases.
    """
    try:
        detected_biases = []
        async for msg in fp.stream_request(
            request, "GPT-3.5-Turbo", create_prompt("bias_detection", topic=argument)
        ):
            for bias in COMMON_BIASES:
                if bias.lower() in msg.text.lower():
                    detected_biases.append(bias)
        return detected_biases
    except Exception as e:
        logger.error(f"Error in detect_specific_biases: {e}")
        return []


async def explain_bias(request: fp.QueryRequest, bias: str, argument: str) -> str:
    """
    Explains how a specific cognitive bias is manifested in the argument.

    Parameters:
        request (fp.QueryRequest): The request object.
        bias (str): The cognitive bias to explain.
        argument (str): The argument being analyzed.

    Returns:
        str: An explanation of how the bias manifests in the argument.
    """
    try:
        explanation_prompt = (
            f"Explain how the {bias} is manifested in the following argument: "
            f"{argument}"
        )
        explanation = ""
        async for msg in fp.stream_request(
            request, "Claude-instant", explanation_prompt
        ):
            explanation += msg.text
        return explanation
    except Exception as e:
        logger.error(f"Error in explain_bias: {e}")
        return "An error occurred while explaining the bias."


async def suggest_debiasing_strategies(
    request: fp.QueryRequest, biases: List[str]
) -> AsyncIterable[fp.PartialResponse]:
    """
    Suggests strategies to mitigate identified cognitive biases.

    Parameters:
        request (fp.QueryRequest): The request object.
        biases (List[str]): The list of biases to address.

    Yields:
        AsyncIterable[fp.PartialResponse]: Suggested strategies for mitigating biases.
    """
    try:
        prompt = (
            f"Suggest strategies to mitigate the following cognitive biases: "
            f"{', '.join(biases)}"
        )
        async for msg in fp.stream_request(request, "GPT-4", prompt):
            yield fp.PartialResponse(text=msg.text)
    except Exception as e:
        logger.error(f"Error in suggest_debiasing_strategies: {e}")
        yield fp.PartialResponse(
            text="An error occurred while suggesting debiasing strategies."
        )


async def get_user_choice(request: fp.QueryRequest) -> str:
    """
    Gets user choice using WebSocket or another method.

    Parameters:
        request (fp.QueryRequest): The request object.

    Returns:
        str: The user's choice.
    """
    # Implement this function based on your framework (e.g., WebSocket, HTTP request, etc.)
    # Example using WebSocket (replace with your actual implementation)
    # async for message in request.websocket:
    #     user_choice = message.text
    #     return user_choice
    return "1"  # Placeholder return value
