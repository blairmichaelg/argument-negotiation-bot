# core/__init__.py

from .debate import handle_functionality as handle_debate, process_functionality as process_debate
from .negotiation import handle_functionality as handle_negotiation, process_functionality as process_negotiation
from .fact_check import handle_functionality as handle_fact_check, process_functionality as process_fact_check
from .bias_detection import handle_functionality as handle_bias_detection, process_functionality as process_bias_detection
from .contract_analysis import handle_functionality as handle_contract_analysis, process_functionality as process_contract_analysis
from .salary_negotiation import handle_functionality as handle_salary_negotiation, process_functionality as process_salary_negotiation

__all__ = [
    "handle_debate",
    "process_debate",
    "handle_negotiation",
    "process_negotiation",
    "handle_fact_check",
    "process_fact_check",
    "handle_bias_detection",
    "process_bias_detection",
    "handle_contract_analysis",
    "process_contract_analysis",
    "handle_salary_negotiation",
    "process_salary_negotiation",
]