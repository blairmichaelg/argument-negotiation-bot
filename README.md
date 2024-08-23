# Argument and Negotiation Master Bot

This bot is designed to assist with debates, negotiations, fact-checking, cognitive bias detection, contract analysis, and salary negotiations.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Argument and Negotiation Master Bot is a versatile tool designed to assist users in various scenarios such as debates, negotiations, fact-checking, cognitive bias detection, contract analysis, and salary negotiations. It leverages advanced AI models to provide insightful and accurate responses.

## Features

- **Debate Assistance**: Generate and analyze arguments for and against a given topic.
- **Negotiation Support**: Provide negotiation tactics and analyze offers.
- **Fact-Checking**: Verify the accuracy of statements.
- **Cognitive Bias Detection**: Identify cognitive biases in arguments.
- **Contract Analysis**: Analyze contract clauses for potential issues.
- **Salary Negotiation**: Offer advice on salary negotiations.

## Project Structure

```markdown
argument-negotiation-bot/
├── __pycache__/
├── .flake8
├── .gitignore
├── .pre-commit-config.yaml
├── .pytest_cache/
│   ├── .gitignore
│   ├── CACHEDIR.TAG
│   ├── README.md
│   └── v/
├── .vscode/
│   └── settings.json
├── core/
│   ├── __init__.py
│   ├── __pycache__/
│   ├── bias_detection.py
│   ├── contract_analysis.py
│   ├── debate.py
│   ├── fact_check.py
│   ├── negotiation.py
│   └── salary_negotiation.py
├── improvement-deployment-plan.md
├── LICENSE
├── main.py
├── modal_deploy.py
├── overall-development-plan
├── PoeServerBotGuide.txt
├── pyproject.toml
├── README.md
├── requirements.in
├── requirements.txt
├── server-bot-quick-start/
│   ├── .flake8
│   └── ...
├── tests/
│   ├── __init__.py
│   ├── __pycache__/
│   ├── test_bias_detection.py
│   ├── test_contract_analysis.py
│   ├── test_debate.py
│   ├── test_fact_check.py
│   ├── test_negotiation.py
│   └── test_salary_negotiation.py
├── utils/
│   ├── __init__.py
│   ├── __pycache__/
│   ├── database.py
│   ├── error_handling.py
│   ├── external_api.py
│   ├── helpers.py
│   └── prompt_engineering.py
├── venv/
│   └──
```

## Installation

1. **Clone the repository**:

    ```sh
    git clone https://github.com/yourusername/argument-negotiation-bot.git
    cd argument-negotiation-bot
    ```

2. **Install dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

3. **Set up pre-commit hooks**:

    ```sh
    pre-commit install
    ```

## Usage

1. **Run the bot locally**:

    ```sh
    uvicorn main:app --reload
    ```

2. **Interact with the bot**:
    Access the bot at [`http://localhost:8000`](http://localhost:8000) and use the `/process` endpoint to send messages.

## Configuration

- **Environment Variables**:
  - `DATABASE_URL`: URL for

 the

 database connection.
    - `OPENAI_API_KEY`: API key for OpenAI.

- **Logging Configuration**:
    Configure logging settings in [`main.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fc%3A%2FUsers%2FProjects%2Fargument-negotiation-bot%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "c:\Users\Projects\argument-negotiation-bot\main.py") using the `configure_logging` function.

## Deployment

We recommend using Modal for deployment. Follow these steps:

1. **Install the Modal client**:

    ```sh
    pip install modal-client
    ```

2. **Set up your Modal token**:

    ```sh
    modal token new --source poe
    ```

3. **Deploy to Modal**:

    ```sh
    git clone https://github.com/poe-platform/server-bot-quick-start
    cd server-bot-quick-start
    pip install -r requirements.txt
    modal deploy echobot.py
    ```

## Testing

1. **Run unit tests**:

    ```sh
    pytest
    ```

2. **Test individual functionalities**:
    Each core functionality has its own test file in the [`tests/`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fc%3A%2FUsers%2FProjects%2Fargument-negotiation-bot%2Ftests%2F%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "c:\Users\Projects\argument-negotiation-bot\tests\") directory.

## Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**.
2. **Create a new branch**:

    ```sh
    git checkout -b feature/your-feature-name
    ```

3. **Make your changes**.
4. **Commit your changes**:

    ```sh
    git commit -m "Add your commit message"
    ```

5. **Push to the branch**:

    ```sh
    git push origin feature/your-feature-name
    ```

6. **Create a Pull Request**.

## License

This project is licensed under the 3-Clause BSD License. See the [`LICENSE`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fc%3A%2FUsers%2FProjects%2Fargument-negotiation-bot%2FLICENSE%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "c:\Users\Projects\argument-negotiation-bot\LICENSE") file for details.

Feel free to customize this README further based on your specific needs and additional details about your project.
