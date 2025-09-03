# Contributing to AI Shell

Thank you for your interest in contributing to AI Shell! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/Ai_shell.git`
3. Create a virtual environment: `python3 -m venv venv && source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Install development dependencies: `pip install pytest black flake8`

## Development Setup

### Project Structure

```
ai_shell/
├── ai_shell/           # Main package
│   ├── __init__.py
│   ├── main.py         # Application entry point
│   ├── config.py       # Configuration management
│   ├── llm.py          # LLM integration
│   ├── executor.py     # Command execution and security
│   └── ui.py           # User interface utilities
├── tests/              # Test suite
├── setup.py            # Package setup
├── requirements.txt    # Dependencies
└── README.md
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_config.py

# Run with coverage
python -m pytest --cov=ai_shell
```

### Code Style

We use Black for code formatting and flake8 for linting:

```bash
# Format code
black ai_shell/ tests/

# Check code style
flake8 ai_shell/ tests/
```

## Contributing Guidelines

### Pull Requests

1. Create a feature branch from `main`
2. Make your changes
3. Add tests for new functionality
4. Ensure all tests pass
5. Format your code with Black
6. Submit a pull request

### Commit Messages

Use clear, descriptive commit messages:
- `feat: add new security validation feature`
- `fix: resolve issue with command execution`
- `docs: update installation instructions`
- `test: add tests for configuration module`

### Adding New Features

1. **LLM Providers**: Add new providers in `llm.py` by extending the `LLMProvider` base class
2. **Security Checks**: Add new security validations in `executor.py`
3. **Configuration**: Add new config options in `config.py` with appropriate defaults
4. **UI Components**: Add new UI elements in `ui.py`

### Testing

- Write tests for all new functionality
- Maintain high test coverage
- Use descriptive test names
- Include both positive and negative test cases

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow the project's coding standards

## Questions?

Feel free to open an issue if you have questions about contributing!