# Usage Guide

This guide summarizes how to run AI Shell from the command line, select operating modes, and choose the right provider for your environment.

## ⚙️ Command-Line Quick Reference

| Option | Description |
| --- | --- |
| `--mode {translator,assistant,metasploit,wapiti}` | Run a specific mode without the interactive selector. |
| `--provider {gemini,local}` | Choose the LLM backend (Gemini API or local Ollama). |
| `--config <file>` | Path to a custom YAML configuration file. |
| `--api-key <key>` | Override the Gemini API key for this run. |
| `--no-confirmation` | Skip confirmation prompts for generated commands. |
| `--log-level {DEBUG,INFO,WARNING,ERROR}` | Override the logging level. |
| `--version` | Display AI Shell version. |

Configuration precedence follows: **CLI flags → environment variables → `config.yaml` → defaults**.

## 🎯 Operating Modes

### Translator Mode
- Start with `ai-shell --mode translator`.
- Enter natural language prompts and receive a single shell command.
- Commands are validated before execution; type `exit` to quit.

### Assistant Mode
- Start with `ai-shell --mode assistant`.
- Conversational guidance with history; responses may include runnable commands.
- When a command is detected, AI Shell asks for confirmation before running it.

### Metasploit Assistant
- Start with `ai-shell --mode metasploit` (requires `msfconsole`).
- A Metasploit shell opens; prefix prompts with `?` to ask the AI for help.
- Confirm before executing AI-suggested commands; type `exit` inside msfconsole to leave.

### Wapiti Assistant
- Start with `ai-shell --mode wapiti` (requires `wapiti` on PATH).
- Opens a Bash session tailored for web security tasks; prefix prompts with `?` to get AI-generated commands.
- Confirm before execution; exit the shell to return to your terminal.

## 🤖 Provider Setup

### Gemini (Cloud)
1. Export your key: `export GEMINI_API_KEY="your_key"`.
2. Run with `--provider gemini` or set `llm.provider: gemini` in `config.yaml`.
3. You can override the key per run with `--api-key`.

### Local (Ollama)
1. Install Ollama and pull a model (e.g., `ollama pull llama3`).
2. Start AI Shell with `--provider local`; the guided prompt helps select a model and host/port.
3. Connection details are stored in the config for future runs.

## 🛡️ Security & Confirmation

- By default, AI Shell validates commands and asks for confirmation before executing.
- Use `--no-confirmation` for automation or when running in a controlled environment.
- Adjust safety lists in `config.yaml` under `security.dangerous_commands` and `security.safe_commands`.

## 📚 Where to Go Next

- **Configuration details:** [docs/CONFIGURATION.md](CONFIGURATION.md)  
- **Architecture overview:** [docs/ARCHITECTURE.md](ARCHITECTURE.md)  
- **Examples & tutorials:** [docs/EXAMPLES.md](EXAMPLES.md)  
- **Troubleshooting tips:** [docs/TROUBLESHOOTING.md](TROUBLESHOOTING.md)

