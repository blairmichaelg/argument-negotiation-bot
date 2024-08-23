"""Utility modules for the Argument and Negotiation Master Bot."""

from .error_handling import handle_error
from .prompt_engineering import create_prompt, PROMPT_TEMPLATES
from .database import get_db, User, NegotiationScenario
from .helpers import (
    analyze_sentiment,
    generate_dynamic_follow_up_questions,
    extract_job_details,
    format_salary_data,
)
from .external_api import fetch_salary_data

__all__ = [
    "handle_error",
    "create_prompt",
    "PROMPT_TEMPLATES",
    "get_db",
    "User",
    "NegotiationScenario",
    "analyze_sentiment",
    "generate_dynamic_follow_up_questions",
    "extract_job_details",
    "format_salary_data",
    "fetch_salary_data",
]
