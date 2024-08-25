"""Core modules for the Argument and Negotiation Master Bot."""

from .debate import handle_debate
from .negotiation import handle_negotiation
from . import handle_fact_check
from . import handle_bias_detection
from . import handle_contract_analysis
from . import handle_salary_negotiation

from . import error_handling
from utils.prompt_engineering import create_prompt, PROMPT_TEMPLATES

__all__ = [
    "handle_debate",
    "handle_negotiation",
    "handle_fact_check",
    "handle_bias_detection",
    "handle_contract_analysis",
    "handle_salary_negotiation",
    "create_prompt",
    "PROMPT_TEMPLATES",
    "error_handling",
]
