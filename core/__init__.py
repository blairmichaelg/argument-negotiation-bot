""" This module is the entry point for the core package. It imports all the modules that are part of the core package. """

# Importing modules from the core package
import logging

from core import (
    error_handling,
    handle_bias_detection,
    handle_contract_analysis,
    handle_debate,
    handle_fact_check,
    handle_negotiation,
    handle_salary_negotiation,
)
from utils.prompt_engineering import PROMPT_TEMPLATES, create_prompt

# Set the logging level for the setuptools logger to INFO to avoid unnecessary logs during the installation of the package in the user's environment and add a StreamHandler to print the logs to the console.
setuptools_logger = logging.getLogger("setuptools")
setuptools_logger.setLevel(logging.INFO)
setuptools_logger.addHandler(logging.StreamHandler())

# Defining the __all__ variable to control what is imported when using the * syntax
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

# Defining the version of the core package
__version__ = (
    "0.1.0"  # This version number should be updated in every release of the package
)

# Defining the author of the core package
__author__ = "blairmichaelg"  # This author name should be updated in every release of the package

# Defining the author's email address
__author_email__ = "blairmichaelg@gmail.com"  # This email address should be updated in every release of the package"

# Defining the license of the core package
__license__ = "MIT"  # This license should be updated in every release of the package

# Defining the description of the core package
__description__ = "A package that provides functionalities for handling debates, negotiations, fact-checking, bias detection, contract analysis, and salary negotiations."
