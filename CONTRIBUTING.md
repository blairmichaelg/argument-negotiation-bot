# Contributing to Argument & Negotiation Master Bot

First off, thank you for considering contributing to the Argument & Negotiation Master Bot! It's people like you that make this project such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to blairmichaelg@gmail.com.

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

**Before Submitting A Bug Report:**
- Check the [existing issues](https://github.com/blairmichaelg/argument-negotiation-bot/issues) to see if the problem has already been reported
- Collect information about the bug:
  - Stack trace and error messages
  - Steps to reproduce the issue
  - Python version and operating system
  - Any relevant configuration

**How Do I Submit A Good Bug Report?**

Bugs are tracked as [GitHub issues](https://github.com/blairmichaelg/argument-negotiation-bot/issues). Create an issue and provide the following information:

- **Use a clear and descriptive title** for the issue
- **Describe the exact steps to reproduce the problem** in as much detail as possible
- **Provide specific examples** to demonstrate the steps
- **Describe the behavior you observed** after following the steps
- **Explain which behavior you expected to see instead** and why
- **Include screenshots or code snippets** if relevant

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion, including completely new features and minor improvements to existing functionality.

**Before Submitting An Enhancement Suggestion:**
- Check if the enhancement has already been suggested
- Determine which repository the enhancement should be suggested in
- Perform a cursory search to see if the enhancement has already been suggested

**How Do I Submit A Good Enhancement Suggestion?**

Enhancement suggestions are tracked as [GitHub issues](https://github.com/blairmichaelg/argument-negotiation-bot/issues). Create an issue and provide the following information:

- **Use a clear and descriptive title**
- **Provide a step-by-step description** of the suggested enhancement
- **Provide specific examples** to demonstrate the enhancement
- **Describe the current behavior** and **explain the behavior you'd like to see**
- **Explain why this enhancement would be useful**

### Pull Requests

The process described here has several goals:
- Maintain code quality
- Fix problems that are important to users
- Engage the community in working toward the best possible product

**Before Submitting a Pull Request:**

1. Fork the repository and create your branch from `main`
2. If you've added code that should be tested, add tests
3. Ensure the test suite passes
4. Make sure your code lints (follows PEP 8 and project conventions)
5. Update documentation as needed

**Pull Request Process:**

1. **Fork the Repository**

   ```bash
   git clone https://github.com/your-username/argument-negotiation-bot.git
   cd argument-negotiation-bot
   ```

2. **Create a Branch**

   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix-name
   ```

3. **Set Up Development Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pre-commit install
   ```

4. **Make Your Changes**

   - Write clear, concise code
   - Follow existing code style and conventions
   - Add or update tests as needed
   - Update documentation as needed

5. **Test Your Changes**

   ```bash
   # Run the full test suite
   pytest
   
   # Run with coverage
   pytest --cov=core --cov=utils
   
   # Run linting
   flake8 .
   black --check .
   ```

6. **Commit Your Changes**

   ```bash
   git add .
   git commit -m "Add a clear, descriptive commit message"
   ```

   Commit message guidelines:
   - Use the present tense ("Add feature" not "Added feature")
   - Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
   - Limit the first line to 72 characters or less
   - Reference issues and pull requests after the first line

7. **Push to Your Fork**

   ```bash
   git push origin feature/your-feature-name
   ```

8. **Open a Pull Request**

   - Go to the [repository](https://github.com/blairmichaelg/argument-negotiation-bot)
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill in the pull request template with:
     - A clear title
     - Detailed description of changes
     - Related issue numbers
     - Testing performed
     - Screenshots (if applicable)

## Development Guidelines

### Code Style

This project follows Python best practices and PEP 8 guidelines:

- **Naming Conventions:**
  - `snake_case` for functions, variables, and module names
  - `PascalCase` for class names
  - `UPPER_CASE` for constants

- **Code Formatting:**
  - Use [Black](https://github.com/psf/black) for code formatting (line length: 88)
  - Use [isort](https://pycqa.github.io/isort/) for import sorting
  - Follow [Flake8](https://flake8.pycqa.org/) rules for linting

- **Documentation:**
  - Write docstrings for all public modules, functions, classes, and methods
  - Use [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
  - Keep comments clear and concise

### Testing Guidelines

- Write tests for all new features and bug fixes
- Maintain or improve code coverage
- Use descriptive test names that explain what is being tested
- Use pytest fixtures for common test setup
- Mock external API calls in tests

Example test structure:

```python
import pytest
from core.debate import handle_debate

class TestHandleDebate:
    def test_debate_with_valid_topic(self):
        """Test that debate handling works with a valid topic."""
        # Arrange
        topic = "AI in education"
        
        # Act
        result = await handle_debate(request, f"debate {topic}")
        
        # Assert
        assert result is not None
```

### Documentation Guidelines

- Update README.md if you change functionality
- Add docstrings to new functions and classes
- Update inline comments for complex logic
- Keep documentation in sync with code changes

### Git Workflow

We use a simplified Git workflow:

1. `main` - Stable, production-ready code
2. Feature branches - For developing new features or fixes

**Branch Naming:**
- `feature/description` - For new features
- `fix/description` - For bug fixes
- `docs/description` - For documentation updates
- `refactor/description` - For code refactoring

## Project Structure

Understanding the project structure helps you know where to make changes:

```
argument-negotiation-bot/
├── core/                    # Core business logic
│   ├── bias_detection.py
│   ├── contract_analysis.py
│   ├── debate.py
│   ├── fact_check.py
│   ├── negotiation.py
│   └── salary_negotiation.py
├── utils/                   # Utility functions and helpers
│   ├── database.py
│   ├── error_handling.py
│   ├── external_api.py
│   ├── helpers.py
│   └── prompt_engineering.py
├── tests/                   # Test suite
│   ├── test_*.py
├── main.py                  # Application entry point
└── requirements.txt         # Python dependencies
```

## Getting Help

If you need help with contributing:

- Review existing issues and pull requests
- Read the [README.md](README.md) for project overview
- Open a [discussion](https://github.com/blairmichaelg/argument-negotiation-bot/discussions) for questions
- Reach out to maintainers via email

## Recognition

Contributors will be recognized in:
- The project's GitHub contributors page
- Release notes (for significant contributions)
- The README.md acknowledgments section (for major features)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the Argument & Negotiation Master Bot! 🎉
