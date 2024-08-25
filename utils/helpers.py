import re
from typing import List, Dict

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")

sia = SentimentIntensityAnalyzer()


def analyze_sentiment(text: str) -> str:
    """
    Analyzes the sentiment of a given text using NLTK's VADER sentiment analyzer.

    Parameters:
        text (str): The text to analyze.

    Returns:
        str: A string describing the sentiment (positive, negative, neutral, or mixed).
    """
    sentiment = sia.polarity_scores(text)
    if sentiment["compound"] >= 0.05:
        return "positive"
    elif sentiment["compound"] <= -0.05:
        return "negative"
    elif sentiment["compound"] == 0:
        return "neutral"
    else:
        return "mixed"


def generate_dynamic_follow_up_questions(text: str) -> List[str]:
    """
    Generates dynamic follow-up questions based on the provided text.

    Parameters:
        text (str): The text to analyze.

    Returns:
        List[str]: A list of follow-up questions.
    """
    questions = []
    # Extract key nouns and verbs from the text
    tokens = nltk.word_tokenize(text)
    nouns = [word for word, pos in nltk.pos_tag(tokens) if pos.startswith("NN")]
    verbs = [word for word, pos in nltk.pos_tag(tokens) if pos.startswith("VB")]

    # Generate questions based on nouns and verbs
    for noun in nouns:
        questions.append(f"Tell me more about {noun}.")
        questions.append(f"What is the significance of {noun} in this context?")
    for verb in verbs:
        questions.append(f"Why did {verb} happen?")
        questions.append(f"What were the consequences of {verb}?")

    # Remove duplicate questions
    questions = list(set(questions))
    return questions


def extract_job_details(text: str) -> Dict[str, str | None]:
    """
    Extracts job title and location from user input.

    Parameters:
        text (str): The user's input text.

    Returns:
        Dict[str, str | None]: A dictionary containing the extracted job title and location.
    """
    job_title = None
    location = None

    # Use regular expressions to extract job title and location
    job_title_match = re.search(r"I'm looking for a (.*) job", text, re.IGNORECASE)
    if job_title_match:
        job_title = job_title_match.group(1).strip()
    else:
        job_title_match = re.search(r"I'm a (.*)", text, re.IGNORECASE)
        if job_title_match:
            job_title = job_title_match.group(1).strip()

    location_match = re.search(r"in (.*)", text, re.IGNORECASE)
    if location_match:
        location = location_match.group(1).strip()
    else:
        location_match = re.search(r"in the (.*)", text, re.IGNORECASE)
        if location_match:
            location = location_match.group(1).strip()

    return {"job_title": job_title, "location": location}


def format_salary_data(salary_data: dict) -> str:
    """
    Formats salary data for display to the user.

    Parameters:
        salary_data (dict): A dictionary containing salary data.

    Returns:
        str: A formatted string representing the salary data.
    """
    if "error" in salary_data:
        return salary_data["error"]
    else:
        return f"The average salary for this job is {salary_data['average_salary']} {salary_data['currency']}."
