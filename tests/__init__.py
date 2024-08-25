import logging

# Import all test modules to ensure they are discovered by pytest
from .test_bias_detection import TestHandleBiasDetection
from .test_contract_analysis import TestHandleContractAnalysis
from .test_debate import TestHandleDebate
from .test_fact_check import TestFactCheck
from .test_negotiation import TestGenerateBotResponse
from .test_salary_negotiation import TestSalaryNegotiation

# Set up logging
logger = logging.getLogger(__name__)

# Explicitly declare the public symbols that should be exported
__all__ = [
    "TestHandleBiasDetection",
    "TestHandleContractAnalysis",
    "TestHandleDebate",
    "TestFactCheck",
    "TestGenerateBotResponse",
    "TestSalaryNegotiation",
]
