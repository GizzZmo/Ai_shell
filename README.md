# AI Shell 🤖

<div align="center">

**Your Intelligent Command-Line Copilot**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-passing-green.svg)](#testing)

*Transform natural language into powerful shell commands with AI*

[🚀 Quick Start](#quick-start) • [📖 Documentation](#documentation) • [🤝 Contributing](CONTRIBUTING.md) • [🐛 Issues](https://github.com/GizzZmo/Ai_shell/issues)

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

# Specify provider
ai-shell --provider local
ai-shell --provider gemini --api-key your_key

# Use custom config
ai-shell --config myconfig.yaml
```

## 📖 Documentation

### Configuration

The `config.yaml` file allows you to customize AI Shell's behavior:

```yaml
llm:
  provider: gemini  # or 'local'
  gemini:
    api_key: ""
    model: gemini-1.5-flash
  local:
    host: localhost
    port: 11434
    model: llama3

security:
  require_confirmation: true
  dangerous_commands:
    - rm -rf
    - format
    - dd if=

logging:
  level: INFO
  file: ai_shell.log
```

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key
- `AI_SHELL_CONFIG`: Path to custom configuration file

### Security Features

- **Command Validation**: Blocks dangerous commands
- **User Confirmation**: Requires approval before execution
- **Input Sanitization**: Protects against command injection
- **Configurable Restrictions**: Customizable safety lists

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
├── docs/               # Documentation (coming soon)
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