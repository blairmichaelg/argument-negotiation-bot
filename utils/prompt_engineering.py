from typing import Dict, Any

# Dictionary to store prompt templates for different functionalities
PROMPT_TEMPLATES: Dict[str, str] = {
    "debate": "Generate two opposing viewpoints on the topic: {topic}. Provide clear arguments for both sides, citing relevant facts or examples.",
    "negotiation": "Create a realistic negotiation scenario based on: {topic}. Outline the interests, positions, and potential areas for compromise for both parties involved.",
    "fact-check": "Fact-check the following statement, providing a clear verdict and citing credible sources to support your conclusion: {topic}",
    "bias_detection": "Analyze the following argument for cognitive biases: {topic}. Identify specific biases, explain how they manifest in the argument, and suggest ways to mitigate their influence.",
    "contract_analysis": "Analyze the following contract clause, highlighting key terms, potential risks, and suggesting improvements for clarity and fairness: {topic}",
    "salary_negotiation": "Provide comprehensive salary negotiation advice for someone with these job details: {topic}. Include market data, effective negotiation strategies, potential talking points, and how to handle common counter-offers.",
    "continue_negotiation": "You are negotiating in the following scenario: {topic}\n\nThe user has made the following offer: {user_offer}\n\nPrevious offers: {user_offers}\n\nPrevious bot responses: {bot_responses}\n\nGenerate a realistic and strategic response to the user's offer, considering the negotiation context and previous interactions.",
}


def create_prompt(functionality: str, **kwargs: Any) -> str:
    """
    Creates a formatted prompt for the specified functionality.

    Parameters:
        functionality (str): The name of the functionality for which to create a prompt.
        **kwargs: Additional keyword arguments to format the prompt.

    Returns:
        str: The formatted prompt string.

    Raises:
        ValueError: If the functionality is not found in the PROMPT_TEMPLATES dictionary.
    """
    try:
        prompt_template = PROMPT_TEMPLATES[functionality]
        return prompt_template.format(**kwargs)
    except KeyError:
        raise ValueError(f"No prompt template found for: {functionality}")
