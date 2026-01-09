# AI Shell 🤖

<div align="center">

**Your Intelligent Command-Line Copilot**

<!-- Core badges -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Release](https://img.shields.io/github/v/release/GizzZmo/Ai_shell?include_prereleases&sort=semver)](https://github.com/GizzZmo/Ai_shell/releases)

<!-- Workflow badges -->
[![CI](https://github.com/GizzZmo/Ai_shell/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/GizzZmo/Ai_shell/actions/workflows/ci.yml)
[![Security](https://github.com/GizzZmo/Ai_shell/actions/workflows/security.yml/badge.svg?branch=main)](https://github.com/GizzZmo/Ai_shell/actions/workflows/security.yml)
[![Documentation](https://github.com/GizzZmo/Ai_shell/actions/workflows/documentation.yml/badge.svg?branch=main)](https://github.com/GizzZmo/Ai_shell/actions/workflows/documentation.yml)
[![Performance](https://github.com/GizzZmo/Ai_shell/actions/workflows/performance.yml/badge.svg?branch=main)](https://github.com/GizzZmo/Ai_shell/actions/workflows/performance.yml)

<!-- Quality badges -->
[![Codecov](https://codecov.io/gh/GizzZmo/Ai_shell/branch/main/graph/badge.svg)](https://codecov.io/gh/GizzZmo/Ai_shell)
[![CodeQL](https://github.com/GizzZmo/Ai_shell/workflows/Security/badge.svg)](https://github.com/GizzZmo/Ai_shell/security/code-scanning)

<!-- Community badges -->
[![GitHub issues](https://img.shields.io/github/issues/GizzZmo/Ai_shell)](https://github.com/GizzZmo/Ai_shell/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/GizzZmo/Ai_shell)](https://github.com/GizzZmo/Ai_shell/pulls)
[![GitHub stars](https://img.shields.io/github/stars/GizzZmo/Ai_shell?style=social)](https://github.com/GizzZmo/Ai_shell/stargazers)

*Transform natural language into powerful shell commands with AI*

[🚀 Quick Start](#quick-start) • [📖 Documentation](#documentation) • [🤝 Contributing](CONTRIBUTING.md)  
[🐛 Issues](https://github.com/GizzZmo/Ai_shell/issues) • [📊 Workflow Status](WORKFLOW_STATUS.md)

</div>

---

## Overview

AI Shell is an intelligent, multi-modal command-line assistant that bridges the gap between natural language and complex shell operations. Powered by Large Language Models (LLMs), it translates your requests into executable commands, provides conversational guidance, and integrates with specialized tools like the Metasploit Framework.

Whether you're a beginner learning the command line or a seasoned expert looking to accelerate your workflow, AI Shell adapts to your needs.

## ✨ Key Features

- **🔄 Multi-Modal Architecture**: Three distinct operating modes for different use cases
- **🧠 Advanced LLM Integration**: Support for both cloud (Gemini) and local (Ollama) models
- **🔒 Security-First Design**: Built-in command validation and user confirmation
- **💬 Conversational Memory**: Context-aware responses with chat history
- **🛠️ Tool Integration**: Native support for penetration testing workflows
- **📊 Learning Capability**: Feedback loop for continuous improvement

## 🎯 Operating Modes

### 1. Command Translator Mode
Transform natural language into precise shell commands.

```bash
> find all files larger than 100MB in my home directory
→ find ~ -type f -size +100M
```

### 2. AI Assistant Mode
Conversational partner for complex command-line tasks with explanations and guidance.

```
You: How can I check which processes are using the most memory?
Assistant: On Linux, you can use the 'ps' command combined with 'sort':

```bash
ps aux --sort=-%mem | head -n 10
```

This lists all running processes, sorts them by memory usage in descending order, and shows the top 10.
```

### 3. Metasploit Assistant Mode
Your personal cybersecurity expert with direct msfconsole integration.

Assistant: You can search for Log4j exploits using the 'search' command:

```bash
search cve:2021-44228
```

Would you like me to run this command for you?
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+** 
- **Metasploit Framework** (optional, for Metasploit mode)
- **Ollama** (optional, for local LLMs)

### Installation

#### Option 1: From Source (Recommended)

```bash
# Clone the repository
git clone https://github.com/GizzZmo/Ai_shell.git
cd Ai_shell

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

#### Option 2: Using Setup Scripts

**Linux/Mac:**
```bash
chmod +x install.sh
./install.sh
```

**Windows:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\install.ps1
```

### Configuration

1. **Copy the example configuration:**
   ```bash
   cp config.yaml.example config.yaml
   ```

2. **Set your API key** (for Gemini):
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```

3. **For local LLMs**, install Ollama:
   ```bash
   # Install Ollama (Linux)
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull a model
   ollama pull llama3
   ```

### Usage

```bash
# Interactive mode selection
ai-shell

# Direct modes
ai-shell --mode translator
ai-shell --mode assistant 
ai-shell --mode metasploit
ai-shell --mode wapiti

# Specify provider
ai-shell --provider local
ai-shell --provider gemini --api-key your_key

# Use custom config
ai-shell --config myconfig.yaml

# Adjust safety and logging
ai-shell --no-confirmation
ai-shell --log-level DEBUG
```

For a full CLI reference and mode-by-mode walkthrough, see [docs/USAGE.md](docs/USAGE.md).

## 📖 Documentation

Browse focused guides:
- [Usage Guide](docs/USAGE.md) — CLI flags, modes, and provider selection  
- [Configuration Guide](docs/CONFIGURATION.md) — config structure, profiles, and templates  
- [Architecture Overview](docs/ARCHITECTURE.md) — component and data-flow diagrams  
- [Examples & Tutorials](docs/EXAMPLES.md) — practical prompts and scripts  
- [Troubleshooting](docs/TROUBLESHOOTING.md) — common fixes and debugging tips  

## 🔧 Development

### Project Structure

```
ai_shell/
├── ai_shell/           # Main package
│   ├── main.py         # Application entry point
│   ├── config.py       # Configuration management
│   ├── llm.py          # LLM integration
│   ├── executor.py     # Command execution and security
│   └── ui.py           # User interface utilities
├── tests/              # Test suite
├── docs/               # Documentation guides
├── setup.py            # Package setup
└── requirements.txt    # Dependencies
```

### Testing

```bash
# Install development dependencies
pip install pytest pytest-cov black flake8

# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=ai_shell
```

### Code Style

```bash
# Format code
black ai_shell/ tests/

# Check style
flake8 ai_shell/ tests/
```

## 🔒 Security

- **API Keys**: Store securely using environment variables
- **Command Review**: Always review before execution
- **Local LLMs**: Consider for sensitive environments
- **Network Security**: Be cautious with cloud providers

## 🔄 CI/CD & Workflow System

AI Shell uses a comprehensive GitHub Actions workflow system to ensure code quality, security, and reliability:

### 🛠️ Automated Workflows

#### **Continuous Integration (CI)**
- ✅ **Multi-OS Testing**: Tests run on Ubuntu, Windows, and macOS
- ✅ **Python Versions**: Supports Python 3.9, 3.10, 3.11, and 3.12
- ✅ **Code Quality**: Automated linting with flake8 and formatting checks with black
- ✅ **Test Coverage**: pytest with coverage reporting to Codecov
- ✅ **Package Installation**: Validates the package can be installed and used

#### **Security Scanning**
- 🔒 **CodeQL Analysis**: Advanced code security scanning with extended queries
- 🔒 **Dependency Scanning**: Automated vulnerability checks using Safety
- 🔒 **Secrets Detection**: Trivy scans for exposed secrets in the codebase
- 🔒 **License Compliance**: Verifies all dependencies use compatible licenses
- 🔒 **Scheduled Scans**: Daily security checks to catch new vulnerabilities

#### **Documentation**
- 📖 **Markdown Validation**: Ensures all documentation is syntactically correct
- 📖 **Link Checking**: Validates internal and external links
- 📖 **Code Example Testing**: Verifies Python code examples in documentation
- 📖 **Automated Deployment**: Builds and deploys docs to GitHub Pages with MkDocs
- 📖 **Material Theme**: Beautiful, searchable documentation site

#### **Performance Monitoring**
- ⚡ **Benchmark Tests**: Measures performance of core components
- ⚡ **Memory Profiling**: Tracks memory usage and detects leaks
- ⚡ **Response Time Monitoring**: Ensures operations meet performance targets
- ⚡ **Weekly Runs**: Regular performance regression testing

#### **Release Automation**
- 🚀 **Automated Releases**: Tag-based releases to GitHub and PyPI
- 🚀 **Changelog Generation**: Automatic changelog from git commits
- 🚀 **Package Building**: Builds and validates distribution packages
- 🚀 **Pre-release Support**: Handles alpha, beta, and RC releases

#### **Smart Automation**
- 🏷️ **Auto-labeling**: Automatically labels issues and PRs based on content
- 🏷️ **Size Detection**: Labels PRs by change size (XS, S, M, L, XL)
- 🏷️ **Component Detection**: Labels based on changed files and components
- 📊 **Status Dashboard**: Daily workflow status reports and repository statistics

### 📊 Workflow Status

Check our [Workflow Status Dashboard](WORKFLOW_STATUS.md) for real-time status of all workflows, or view the [Actions tab](https://github.com/GizzZmo/Ai_shell/actions) for detailed run history.

### 🔧 Running Workflows Locally

You can run tests and checks locally before pushing:

```bash
# Run tests
python -m pytest tests/ -v --cov=ai_shell

# Check code style
flake8 ai_shell/ tests/
black --check ai_shell/ tests/

# Run security checks
pip install safety
safety check

# Run performance benchmarks
python -m pytest tests/benchmarks/ --benchmark-only
```

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Steps

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini** for powerful language model capabilities
- **Ollama** community for local LLM support
- **Metasploit Framework** for penetration testing integration

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/GizzZmo/Ai_shell/issues)
- **Discussions**: [GitHub Discussions](https://github.com/GizzZmo/Ai_shell/discussions)

---

**⚠️ Disclaimer**: AI Shell executes system commands. Always review commands before execution and use appropriate security measures. The developers are not responsible for any damage caused by misuse of this tool.
```bash
You: ? search for exploits related to the log4j vulnerability
