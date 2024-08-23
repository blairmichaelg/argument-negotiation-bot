import pytest
import logging

# Import all test modules to ensure they are discovered by pytest
from .test_bias_detection import TestHandleBiasDetection
from .test_contract_analysis import TestHandleContractAnalysis
from .test_debate import TestHandleDebate
from .test_fact_check import TestFactCheck
from .test_negotiation import TestGenerateBotResponse
from .test_salary_negotiation import TestSimulateNegotiation

# Set up logging
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def setup_session():
    # Instantiate each test class to ensure they are used
    test_bias_detection = TestHandleBiasDetection()
    test_contract_analysis = TestHandleContractAnalysis()
    test_debate = TestHandleDebate()
    test_fact_check = TestFactCheck()
    test_negotiation = TestGenerateBotResponse()
    test_salary_negotiation = TestSimulateNegotiation()

    # Log the instantiation to demonstrate usage
    logger.info("TestHandleBiasDetection instance created: %s", test_bias_detection)
    logger.info(
        "TestHandleContractAnalysis instance created: %s", test_contract_analysis
    )
    logger.info("TestHandleDebate instance created: %s", test_debate)
    logger.info("TestFactCheck instance created: %s", test_fact_check)
    logger.info("TestGenerateBotResponse instance created: %s", test_negotiation)
    logger.info("TestSimulateNegotiation instance created: %s", test_salary_negotiation)

    # Perform any setup required for the test session
    pass
