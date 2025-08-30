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

🛠️ Setup & Usage
Prerequisites
Python 3.8+

Metasploit Framework: Required only for the Metasploit Assistant mode. Ensure msfconsole is in your system's PATH.

Ollama (Optional): Required for running local LLMs.

Installation
Clone the repository:

git clone <repository-url>
cd ai-shell

Install Python dependencies:

pip install -r requirements.txt 
# Or manually: pip install google-generativeai requests

Configuration
LLM Provider: On startup, you will be prompted to choose between Gemini (cloud) or a Local LLM (Ollama).

API Key (for Gemini): If you choose Gemini, you will be prompted for your API key. You can also set it as an environment variable to avoid entering it each time:

export API_KEY="your_gemini_api_key_here"

Local Model (for Ollama): If you choose a local LLM, the script will guide you through selecting a model and will automatically pull it if it's not already installed.

Running the Application
Simply execute the Python script:

python ai_shell_metasploit.py

Follow the on-screen prompts to select your desired operating mode and LLM provider.
