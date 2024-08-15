from .debate import handle_debate
from .negotiation import handle_negotiation
from .fact_check import handle_fact_check
from .bias_detection import handle_bias_detection
from .contract_analysis import handle_contract_analysis
from .salary_negotiation import handle_salary_negotiation

__all__ = [
    "handle_debate",
    "handle_negotiation",
    "handle_fact_check",
    "handle_bias_detection",
    "handle_contract_analysis",
    "handle_salary_negotiation",
]