<div align="center">

# 🤖 Argument & Negotiation Master Bot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

*An AI-powered bot that helps you master debates, negotiations, fact-checking, and more.*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 📖 Overview

The **Argument & Negotiation Master Bot** is a versatile AI-powered assistant designed to help users navigate complex conversational scenarios. Built on FastAPI and leveraging advanced language models, it provides intelligent support for debates, negotiations, fact-checking, cognitive bias detection, contract analysis, and salary negotiations.

## ✨ Features

### 🎯 Core Capabilities

- **💬 Debate Assistance** - Generate compelling arguments for both sides of any topic, practice counterarguments, and refine your debating skills
- **🤝 Negotiation Support** - Receive strategic negotiation tactics, analyze offers, and craft persuasive responses
- **✅ Fact-Checking** - Verify the accuracy of statements and claims with AI-powered analysis
- **🧠 Cognitive Bias Detection** - Identify logical fallacies and cognitive biases in arguments to strengthen reasoning
- **📄 Contract Analysis** - Review contract clauses for potential issues, legal implications, and improvement suggestions
- **💰 Salary Negotiation** - Get data-driven advice for salary negotiations with market insights

### 🛠️ Technical Highlights

- Built with **FastAPI** for high-performance async API handling
- Integration with multiple AI models (GPT-4, GPT-3.5-Turbo, Claude)
- Comprehensive test coverage with pytest
- Database integration with SQLAlchemy
- Error handling and logging
- Pre-commit hooks for code quality
- Ready for deployment on Modal

## 🚀 Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![NLTK](https://img.shields.io/badge/NLTK-154f3c?style=for-the-badge&logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)

**Core Technologies:**
- **FastAPI** - Modern, fast web framework for building APIs
- **fastapi-poe** - Poe Platform integration for bot deployment
- **SQLAlchemy** - SQL toolkit and ORM
- **NLTK** - Natural Language Processing toolkit
- **aiohttp** - Async HTTP client/server
- **Modal** - Serverless deployment platform

## 📦 Installation

### Prerequisites

- Python 3.12 or higher
- pip package manager
- (Optional) Virtual environment tool

### Quick Start

1. **Clone the repository**

```bash
git clone https://github.com/blairmichaelg/argument-negotiation-bot.git
cd argument-negotiation-bot
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up pre-commit hooks** (optional but recommended)

```bash
pre-commit install
```

5. **Configure environment variables**

Create a `.env` file in the project root:

```env
DATABASE_URL=sqlite:///./argument_negotiation_bot.db
ADZUNA_API_ID=your_api_id_here
ADZUNA_API_KEY=your_api_key_here
```

## 🎮 Usage

### Running Locally

Start the development server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The bot will be available at `http://localhost:8000`

### Interacting with the Bot

The bot responds to keyword-based requests. Here are some examples:

- **Debate**: "Help me debate the topic: Should AI replace human jobs?"
- **Negotiation**: "I need help with negotiation tactics for a business deal"
- **Fact-check**: "Can you fact-check this statement: The Earth is flat"
- **Cognitive bias**: "Identify cognitive biases in this argument: ..."
- **Contract**: "Analyze this contract clause: ..."
- **Salary**: "Help me negotiate a salary for a Software Engineer position in San Francisco"

### API Endpoints

The bot implements the Poe Protocol and provides standard endpoints for message processing. See the [Poe Server Bot Guide](https://creator.poe.com/docs/server-bots-introduction) for details.

## 🧪 Testing

Run the full test suite:

```bash
pytest
```

Run specific test modules:

```bash
pytest tests/test_debate.py
pytest tests/test_negotiation.py
```

Run with coverage:

```bash
pytest --cov=core --cov=utils --cov-report=html
```

## 📚 Documentation

### Project Structure

```
argument-negotiation-bot/
├── core/                    # Core functionality modules
│   ├── bias_detection.py    # Cognitive bias detection
│   ├── contract_analysis.py # Contract review and analysis
│   ├── debate.py            # Debate assistance
│   ├── fact_check.py        # Fact-checking functionality
│   ├── negotiation.py       # Negotiation support
│   └── salary_negotiation.py # Salary negotiation advice
├── utils/                   # Utility modules
│   ├── database.py          # Database models and operations
│   ├── error_handling.py    # Error handling utilities
│   ├── external_api.py      # External API integrations
│   ├── helpers.py           # Helper functions
│   └── prompt_engineering.py # AI prompt templates
├── tests/                   # Test suite
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
└── pyproject.toml          # Project configuration
```

### Configuration

Key configuration options in `main.py`:

- **Bot Dependencies**: Configure which AI models to use
- **Logging**: Adjust logging levels and handlers
- **Database**: Configure database connection settings

## 🚢 Deployment

### Deploy to Modal

The bot is designed for easy deployment on Modal:

1. **Install Modal**

```bash
pip install modal
```

2. **Set up Modal authentication**

```bash
modal token new --source poe
```

3. **Configure secrets in Modal dashboard**

Add the following secrets in your Modal dashboard:
- `ADZUNA_API_ID`
- `ADZUNA_API_KEY`
- `DATABASE_URL`

4. **Deploy**

```bash
modal deploy main.py
```

### Other Deployment Options

The bot can also be deployed to:
- **Heroku**: Use the included `Procfile` (if present) or create one
- **AWS Lambda**: With appropriate serverless adapters
- **Docker**: Containerize the application for any platform

## 🤝 Contributing

We welcome contributions from the community! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on:

- Code of Conduct
- Development setup
- Pull request process
- Coding standards

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [Poe Platform](https://poe.com/)
- AI models from OpenAI and Anthropic
- Salary data from [Adzuna API](https://developer.adzuna.com/)

## 📧 Contact

**Blair Michael G** - [@blairmichaelg](https://github.com/blairmichaelg)

Project Link: [https://github.com/blairmichaelg/argument-negotiation-bot](https://github.com/blairmichaelg/argument-negotiation-bot)

---

<div align="center">
Made with ❤️ by the community
</div>
