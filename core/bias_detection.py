from typing import AsyncIterable, List
import fastapi_poe as fp
from utils.prompt_engineering import create_prompt

COMMON_BIASES = [
    "Confirmation Bias", "Anchoring Bias", "Availability Heuristic", "Framing Effect",
    "Dunning-Kruger Effect", "Bandwagon Effect", "Negativity Bias", "Sunk Cost Fallacy"
]

async def handle_bias_detection(request: fp.QueryRequest, user_input: str, user_data: dict) -> AsyncIterable[fp.PartialResponse]:
    """Handles user requests for cognitive bias detection."""

    argument = user_input.replace("cognitive bias", "").strip()
    prompt = create_prompt("bias_detection", topic=argument)

    yield fp.PartialResponse(text="Analyzing the argument for cognitive biases...\n\n")

    # Initial bias detection
    async for msg in fp.stream_request(request, "GPT-4", prompt=prompt
        yield fp.PartialResponse(text=msg.text)

    # Detailed bias analysis
    detected_biases = await detect_specific_biases(request, argument)

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
    user_choice = await request.get_next_message()
    if "1" in user_choice.content or "mitigate" in user_choice.content.lower():
        async for msg in await suggest_debiasing_strategies(request, detected_biases):
            yield msg
    elif "2" in user_choice.content or "analyze" in user_choice.content.lower():
        yield fp.PartialResponse(text="Okay, please provide the new argument.")
        # ... (Handle the new argument analysis - re-use this function)
    else:
        yield fp.PartialResponse(text="Alright, what else would you like to do?")
        # ... (Handle other functionalities or end the interaction)

async def detect_specific_biases(request: fp.QueryRequest, argument: str) -> List[str]:
    bias_prompt = f"Identify which of the following cognitive biases are present in this argument: {', '.join(COMMON_BIASES)}\n\nArgument: {argument}"
    detected_biases = []
    async for msg in fp.stream_request(request, "GPT-3.5-Turbo", prompt=bias_prompt):
        # Parse the response to extract biases (improve parsing logic)
        for bias in COMMON_BIASES:
            if bias.lower() in msg.text.lower():
                detected_biases.append(bias)
    return detected_biases

async def explain_bias(request: fp.QueryRequest, bias: str, argument: str) -> str:
    explanation_prompt = f"Explain how the {bias} is manifested in the following argument: {argument}"
    explanation = ""
    async for msg in fp.stream_request(request, "Claude-instant", prompt=explanation_prompt):
        explanation += msg.text
    return explanation

async def suggest_debiasing_strategies(request: fp.QueryRequest, biases: List[str]) -> AsyncIterable[fp.PartialResponse]:
    prompt = f"Suggest strategies to mitigate the following cognitive biases: {', '.join(biases)}"
    async for msg in fp.stream_request(request, "GPT-4", prompt=prompt):
        yield fp.PartialResponse(text=msg.text)