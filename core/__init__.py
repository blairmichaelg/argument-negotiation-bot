"""Utility modules for the Argument and Negotiation Master Bot."""

from .debate import handle_debate
from .negotiation import handle_negotiation
from .fact_check import handle_fact_check
from .bias_detection import handle_bias_detection
from .contract_analysis import handle_contract_analysis
from .salary_negotiation import handle_salary_negotiation
from . import error_handling
from . import error_handling
from error_handling import handle_error
from . import prompt_engineering
from prompt_engineering import create_prompt, PROMPTS

__all__ = [
    "handle_debate",
    "handle_negotiation",
    "handle_fact_check",
    "handle_bias_detection",
    "handle_contract_analysis",
    "handle_salary_negotiation",
    "handle_error",
    "create_prompt",
    "PROMPTS",
]
