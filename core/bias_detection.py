from typing import AsyncIterable, List, Dict
import fastapi_poe as fp
from utils.prompt_engineering import create_prompt
import logging

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
        if argument:
            prompt = create_prompt("bias_detection", topic=argument)
        else:
            prompt = create_prompt("bias_detection")
        yield fp.PartialResponse(
            text="Analyzing the argument for cognitive biases...\n\n"
        )

        # Initial bias detection
        async for msg in fp.stream_request(request, "GPT-4"):
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
            yield fp.PartialResponse(text=f"{bias}:\n{explanation}\n\n")

        yield fp.PartialResponse(
            text="\n\nWould you like to: \n"
            "1. Explore strategies to mitigate these biases?\n"
            "2. Analyze another argument?\n"
            "3. Do something else?"
        )

        # Handle user choice
        user_choice = request.query[-1].content
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
        bias_prompt = f"Identify which of the following cognitive biases are present in this argument: {', '.join(COMMON_BIASES)}\n\nArgument: {argument}"
        detected_biases = []
        async for msg in fp.stream_request(request, "GPT-3.5-Turbo"):
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
        explanation_prompt = f"Explain how the {bias} is manifested in the following argument: {argument}"
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
        prompt = f"Suggest strategies to mitigate the following cognitive biases: {', '.join(biases)}"
        async for msg in fp.stream_request(request, "GPT-4"):
            yield fp.PartialResponse(text=msg.text)
    except Exception as e:
        logger.error(f"Error in suggest_debiasing_strategies: {e}")
        yield fp.PartialResponse(
            text="An error occurred while suggesting debiasing strategies."
        )
