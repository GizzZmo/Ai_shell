AI Shell: Your Command-Line Copilot
AI Shell is an intelligent, multi-modal command-line assistant designed to bridge the gap between natural language and complex shell operations. It leverages the power of Large Language Models (LLMs) to translate your requests into executable commands, assist with conversational guidance, and even integrate with specialized tools like the Metasploit Framework.

Whether you're a beginner learning the ropes or a seasoned expert looking to accelerate your workflow, AI Shell is your ultimate command-line copilot.

🚀 Evolution: From Simple Translator to Powerful Assistant
The journey from version 0.0.3 to the current release marks a significant architectural and functional leap. The tool has evolved from a basic single-purpose translator into a sophisticated, multi-tool platform.

Key Enhancements Since v0.0.3:
Multi-Modal Architecture: The single "translator" mode has been expanded into three distinct operating modes:

Command Translator: The original, direct prompt -> command functionality.

AI Assistant: A conversational, stateful chat mode for general assistance, explanations, and multi-step tasks.

Metasploit Assistant: A specialized mode that launches msfconsole in an interactive session, with an AI expert ready to guide your penetration testing workflow.

Interactive Tool Integration: The most significant architectural change is the move from basic subprocess calls to a pseudoterminal (pty). This allows AI Shell to run and interact with stateful, persistent applications like msfconsole, capturing real-time output and maintaining the tool's internal state (e.g., set variables, active modules).

Advanced LLM Interaction:

Specialized System Prompts: Each mode now uses a unique, carefully crafted system prompt that primes the LLM for the specific context (general shell vs. Metasploit).

Conversational Memory: The Assistant and Metasploit modes maintain a chat history, allowing for follow-up questions and context-aware responses.

Enhanced Local LLM Support (Ollama):

Setup and model pulling is now automated.

The script checks for available memory and provides a menu of well-tested local models.

Data-Driven Improvement: A feedback loop (log_training_pair) has been introduced, allowing users to confirm correct commands or provide corrections. This creates a valuable dataset for future fine-tuning of the AI model.

Improved User Experience: The command execution now streams output in real-time, providing a much better experience for long-running processes. The UI has been enhanced with more distinct colors and clearer instructions.

🔥 Core Features & Operating Modes
1. Command Translator Mode
The classic AI Shell experience. Describe what you want to do in plain English, and the AI will provide the exact shell command.

Input: > find all files larger than 100MB in my home directory

Output: find ~ -type f -size +100M

2. AI Assistant Mode
A conversational partner for your command-line tasks. Ask for explanations, get help with complex workflows, or have the AI generate commands in a chat-like interface.

You: How can I check which processes are using the most memory?

Assistant: On Linux, you can use the 'ps' command combined with 'sort'. Here is a command that should work for you: \``bash
ps aux --sort=-%mem | head -n 10
```
This command lists all running processes, sorts them by memory usage in descending order, and shows you the top 10.`

3. Metasploit Assistant Mode
Your personal cybersecurity expert. This mode launches an interactive msfconsole session and provides an AI assistant that is specifically trained to help with penetration testing tasks.

Direct Interaction: Type any msfconsole command directly.

AI Guidance: Prefix your request with ? to ask the AI for help.

Input: ? search for exploits related to the log4j vulnerability

Assistant: Of course. You can search for Log4j exploits using the 'search' command. Here is a precise command: \``bash
search cve:2021-44228
```
Would you like me to run this command for you?`

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** 
- **Metasploit Framework** (optional, for Metasploit mode)
- **Wapiti** (optional, for web application scanning)
- **Ollama** (optional, for local LLMs)

### Installation

#### Option 1: From Source (Recommended)

```bash
# Clone the repository
git clone https://github.com/GizzZmo/Ai_shell.git
cd Ai_shell

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
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
   Or edit `config.yaml` directly.

3. **For local LLMs**, ensure Ollama is installed:
   ```bash
   # Install Ollama (Linux)
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull a model
   ollama pull llama3
   ```

### Usage

#### Command Line Interface

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

# Skip confirmations (be careful!)
ai-shell --no-confirmation
```

#### Python Module

```python
from ai_shell.main import main
from ai_shell.config import get_config

# Run the application
main()

# Or use components directly
config = get_config()
print(f"Current provider: {config.get('llm.provider')}")
```

## 📚 Documentation

### Configuration File

The `config.yaml` file allows you to customize AI Shell's behavior:

```yaml
llm:
  provider: gemini  # or 'local'
  gemini:
    api_key: ""  # Your Gemini API key
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

AI Shell includes several security features to protect your system:

- **Command Validation**: Blocks known dangerous commands
- **User Confirmation**: Requires confirmation before executing commands
- **Input Sanitization**: Protects against command injection
- **Configurable Restrictions**: Customize dangerous command lists

## 🧪 Development

### Running Tests

```bash
# Install development dependencies
pip install pytest pytest-cov

# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=ai_shell
```

### Code Formatting

```bash
# Install formatting tools
pip install black flake8

# Format code
black ai_shell/ tests/

# Check style
flake8 ai_shell/ tests/
```

### Project Structure

```
ai_shell/
├── ai_shell/           # Main package
│   ├── __init__.py     # Package initialization
│   ├── main.py         # Application entry point
│   ├── config.py       # Configuration management
│   ├── llm.py          # LLM integration
│   ├── executor.py     # Command execution and security
│   └── ui.py           # User interface utilities
├── tests/              # Test suite
│   ├── conftest.py     # Test configuration
│   ├── test_config.py  # Configuration tests
│   └── ...             # Other test modules
├── setup.py            # Package setup
├── requirements.txt    # Dependencies
├── config.yaml.example # Example configuration
└── README.md           # This file
```

## 🔒 Security Considerations

- **API Keys**: Store API keys securely using environment variables
- **Command Review**: Always review commands before execution
- **Local LLMs**: Consider using local LLMs for sensitive environments
- **Network Security**: Be cautious when using cloud LLM providers

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini for powerful language model capabilities
- Ollama community for local LLM support
- Metasploit Framework for penetration testing integration
- Wapiti for web application security scanning

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/GizzZmo/Ai_shell/issues)
- **Discussions**: [GitHub Discussions](https://github.com/GizzZmo/Ai_shell/discussions)
- **Documentation**: See the `docs/` directory (coming soon)

---

**⚠️ Disclaimer**: AI Shell is a powerful tool that can execute system commands. Always review commands before execution and use appropriate security measures. The developers are not responsible for any damage caused by misuse of this tool.
