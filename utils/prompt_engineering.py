"""Prompt engineering utilities for the Argument and Negotiation Master Bot."""

from typing import Dict, Any
import json

PROMPTS = {
    "debate": "Generate two opposing viewpoints on the topic: {topic}. "
              "Provide clear arguments for both sides, citing relevant facts or examples.",
    "negotiation": "Create a negotiation scenario based on: {scenario}. "
                   "Outline the interests of both parties and potential areas for compromise.",
    "fact_check": "Fact-check the following statement: {statement}. "
                  "Provide a clear verdict and cite credible sources to support your conclusion.",
    "bias_detection": "Analyze the following argument for cognitive biases: {argument}. "
                      "Identify specific biases and explain how they manifest in the argument.",
    "contract_analysis": "Analyze the following contract clause: {clause}. "
                         "Highlight key terms, potential risks, and suggest improvements.",
    "salary_negotiation": "Provide salary negotiation advice for: {job_details}. "
                          "Include market data, negotiation strategies, and potential talking points."
}

def create_prompt(functionality: str, **kwargs: Any) -> str:
    """
    Create a prompt for a specific functionality.

    Args:
        functionality (str): The name of the functionality.
        **kwargs: Keyword arguments to format the prompt.

    Returns:
        str: Formatted prompt for the specified functionality.

    Raises:
        KeyError: If the functionality is not found in PROMPTS.
        ValueError: If required kwargs are missing.
    """
    try:
        prompt_template = PROMPTS[functionality]
        return prompt_template.format(**kwargs)
    except KeyError:
        raise KeyError(f"No prompt template found for functionality: {functionality}")
    raise ValueError(f"Missing required argument for prompt: {str(e)}")

def parse_llm_response(response: str) -> Dict[str, Any]:
    """
    Parse the response from an LLM into a structured format.

    Args:
        response (str): The raw response from the LLM.

    Returns:
        Dict[str, Any]: Structured data extracted from the response.

    Raises:
        ValueError: If the response cannot be parsed.
    """
    try:
        # Attempt to parse as JSON first
        return json.loads(response)
    except json.JSONDecodeError:
        # If not JSON, attempt to parse as key-value pairs
        result = {}
        for line in response.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                result[key.strip()] = value.strip()
        if result:
            return result
        else:
            raise ValueError("Unable to parse LLM response into structured data")

def generate_follow_up_questions(topic: str, context: str) -> list[str]:
    """
    Generate follow-up questions based on the topic and context.

    Args:
        topic (str): The main topic of discussion.
        context (str): The context of the current conversation.

    Returns:
        list[str]: A list of follow-up questions.
    """
    # This is a placeholder. In a real implementation, you might use an LLM to generate these questions.
    questions = [
        f"Can you elaborate on how {topic} affects different stakeholders?",
        f"What are some potential long-term implications of {topic}?",
        f"How does {topic} compare to similar concepts or situations?",
        f"What are some common misconceptions about {topic}?",
    ]
    return questions