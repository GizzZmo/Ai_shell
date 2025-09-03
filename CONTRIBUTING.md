# Contributing to AI Shell

Thank you for your interest in contributing to AI Shell! This document provides comprehensive guidelines for contributing to the project.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of command-line tools
- Familiarity with Python and AsyncIO (for advanced contributions)

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/Ai_shell.git
   cd Ai_shell
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pytest black flake8 pytest-cov
   ```

4. **Install in Development Mode**
   ```bash
   pip install -e .
   ```

5. **Verify Installation**
   ```bash
   python -m pytest
   ai-shell --help
   ```

## 🏗️ Project Architecture

### Core Components

```
ai_shell/
├── main.py         # Application entry point and CLI interface
├── config.py       # Configuration management with YAML support
├── llm.py          # LLM provider abstractions (Gemini, Ollama)
├── executor.py     # Command execution with security validation
└── ui.py           # User interface utilities and formatting
```

### Key Design Patterns

- **Provider Pattern**: LLM providers implement a common interface
- **Configuration Management**: Centralized config with environment variable support
- **Security Layer**: Command validation and user confirmation system
- **Async Architecture**: Non-blocking operations for better UX

## 🔧 Development Workflow

### Before Making Changes

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Run Tests**
   ```bash
   python -m pytest -v
   ```

3. **Check Code Style**
   ```bash
   black --check ai_shell/ tests/
   flake8 ai_shell/ tests/
   ```

### Making Changes

1. **Follow Code Style**
   - Use Black for formatting
   - Follow PEP 8 guidelines
   - Add type hints where appropriate
   - Write descriptive docstrings

2. **Write Tests**
   - Add unit tests for new functionality
   - Maintain high test coverage
   - Use descriptive test names
   - Include both positive and negative test cases

3. **Update Documentation**
   - Update README.md if needed
   - Add docstrings to new functions/classes
   - Update configuration examples

### Testing Guidelines

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_config.py

# Run with coverage
python -m pytest --cov=ai_shell --cov-report=html

# Run tests in verbose mode
python -m pytest -v -s
```

### Code Quality

```bash
# Format code
black ai_shell/ tests/

# Check code style
flake8 ai_shell/ tests/

# Type checking (optional)
mypy ai_shell/
```

## 📝 Contribution Types

### 🐛 Bug Fixes

1. **Report the Bug**
   - Use GitHub Issues
   - Provide clear reproduction steps
   - Include system information
   - Add relevant logs or screenshots

2. **Fix the Bug**
   - Write a failing test first
   - Implement the minimal fix
   - Ensure all tests pass
   - Update documentation if needed

### ✨ New Features

1. **Propose the Feature**
   - Open a GitHub Issue for discussion
   - Explain the use case and benefits
   - Consider the scope and complexity

2. **Implement the Feature**
   - Follow the existing architecture patterns
   - Add comprehensive tests
   - Update documentation
   - Consider backward compatibility

### Common Contribution Areas

#### Adding New LLM Providers

1. Create a new provider class in `llm.py`:
   ```python
   class NewLLMProvider(LLMProvider):
       def __init__(self, config):
           self.config = config
           
       async def generate_response(self, prompt, system_prompt=""):
           # Implementation here
           pass
   ```

2. Register the provider in `get_llm_provider()`
3. Add configuration options
4. Write comprehensive tests

#### Enhancing Security Features

1. Add new validation rules in `executor.py`
2. Update the dangerous commands list
3. Add configuration options for new security features
4. Test edge cases thoroughly

#### Improving User Interface

1. Add new UI components in `ui.py`
2. Ensure consistent styling with existing components
3. Test across different terminal environments
4. Consider accessibility

## 🧪 Testing Strategy

### Test Categories

1. **Unit Tests**: Individual component testing
2. **Integration Tests**: Component interaction testing
3. **End-to-End Tests**: Full workflow testing
4. **Security Tests**: Validation and safety testing

### Writing Good Tests

```python
def test_config_load_from_file():
    """Test that configuration loads correctly from YAML file."""
    # Arrange
    config_data = {"llm": {"provider": "gemini"}}
    
    # Act
    config = Config(config_data)
    
    # Assert
    assert config.get("llm.provider") == "gemini"
```

### Test Coverage

- Aim for >90% test coverage
- Focus on critical paths and edge cases
- Mock external dependencies (APIs, file system)
- Test error conditions and recovery

## 📚 Documentation

### Code Documentation

- **Docstrings**: All public functions and classes
- **Type Hints**: Use for better IDE support
- **Comments**: Explain complex logic, not obvious code

### User Documentation

- **README.md**: Keep updated with new features
- **Configuration**: Document all config options
- **Examples**: Provide practical usage examples

## 🎯 Commit Guidelines

### Commit Message Format

```
type(scope): brief description

Detailed explanation of the change, including:
- Why the change was made
- What was changed
- Any breaking changes or migration notes

Fixes #123
```

### Commit Types

- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring without feature changes
- `test`: Adding or updating tests
- `chore`: Build process or auxiliary tool changes

### Examples

```
feat(llm): add support for Claude API

- Implement ClaudeProvider class
- Add configuration options for Claude
- Update provider selection logic
- Add comprehensive tests

Fixes #456

fix(security): prevent command injection in user input

- Sanitize user input before processing
- Add validation for special characters
- Update security tests
- Document security considerations

Closes #789
```

## 🚢 Release Process

### Pull Request Guidelines

1. **Before Submitting**
   - Ensure all tests pass
   - Update documentation
   - Add changelog entry
   - Squash commits if needed

2. **PR Description**
   - Clear title and description
   - Link to related issues
   - Include screenshots for UI changes
   - List breaking changes

3. **Review Process**
   - Address reviewer feedback
   - Keep discussions focused
   - Be open to suggestions

### Versioning

We follow [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH`
- Major: Breaking changes
- Minor: New features, backward compatible
- Patch: Bug fixes, backward compatible

## 🤝 Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow the project's coding standards
- Focus on the problem, not the person

### Getting Help

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Code Review**: Learn from feedback and review others' code

## 🎉 Recognition

Contributors are recognized in:
- GitHub contributor graphs
- Release notes for significant contributions
- Special mentions for outstanding contributions

Thank you for contributing to AI Shell! 🚀