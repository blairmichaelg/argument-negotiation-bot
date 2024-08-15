from typing import AsyncIterable, List
import fastapi_poe as fp
from utils.prompt_engineering import create_prompt

COMMON_BIASES = [
    "Confirmation Bias", "Anchoring Bias", "Availability Heuristic", "Framing Effect",
    "Dunning-Kruger Effect", "Bandwagon Effect", "Negativity Bias", "Sunk Cost Fallacy"
]

async def handle_functionality(request: fp.QueryRequest, argument: str) -> AsyncIterable[fp.PartialResponse]:
    prompt = create_prompt("bias_detection", argument)
    
    yield fp.PartialResponse(text="Analyzing the argument for cognitive biases...\n\n")
    
    # Initial bias detection
    async for msg in fp.stream_request(request, "GPT-4", request.access_key, prompt=prompt):
        yield fp.PartialResponse(text=msg.text)
    
    # Detailed bias analysis
    detected_biases = await detect_specific_biases(request, argument)
    
    yield fp.PartialResponse(text="\n\nDetailed bias analysis:\n\n")
    for bias in detected_biases:
        explanation = await explain_bias(request, bias, argument)
        yield fp.PartialResponse(text=f"{bias}:\n{explanation}\n\n")
    
    yield fp.PartialResponse(text="Would you like to explore strategies to mitigate these biases or analyze another argument?")

async def detect_specific_biases(request: fp.QueryRequest, argument: str) -> List[str]:
    bias_prompt = f"Identify which of the following cognitive biases are present in this argument: {', '.join(COMMON_BIASES)}\n\nArgument: {argument}"
    detected_biases = []
    async for msg in fp.stream_request(request, "GPT-3.5-Turbo", request.access_key, prompt=bias_prompt):
        # Parse the response to extract biases
        # This is a simplified version; in a real implementation, you'd parse the response more robustly
        for bias in COMMON_BIASES:
            if bias.lower() in msg.text.lower():
                detected_biases.append(bias)
    return detected_biases

async def explain_bias(request: fp.QueryRequest, bias: str, argument: str) -> str:
    explanation_prompt = f"Explain how the {bias} is manifested in the following argument: {argument}"
    async for msg in fp.stream_request(request, "Claude-instant", request.access_key, prompt=explanation_prompt):
        return msg.text  # Return the first (and likely only) message as the explanation

async def process_functionality(argument: str) -> str:
    return f"Detecting bias in argument: {argument}"

async def suggest_debiasing_strategies(request: fp.QueryRequest, biases: List[str]) -> AsyncIterable[fp.PartialResponse]:
    prompt = f"Suggest strategies to mitigate the following cognitive biases: {', '.join(biases)}"
    async for msg in fp.stream_request(request, "GPT-4", request.access_key, prompt=prompt):
        yield fp.PartialResponse(text=msg.text)