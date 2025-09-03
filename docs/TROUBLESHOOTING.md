# Troubleshooting Guide

This guide helps you resolve common issues when using AI Shell.

## 🚨 Common Issues

### Installation Problems

#### Issue: `ModuleNotFoundError: No module named 'ai_shell'`

**Symptoms:**
- Error when running `ai-shell` command
- Python cannot find the ai_shell module

**Solutions:**
1. **Install in development mode:**
   ```bash
   cd Ai_shell
   pip install -e .
   ```

2. **Check Python path:**
   ```bash
   python -c "import sys; print(sys.path)"
   ```

3. **Use virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .
   ```

#### Issue: `pip install` fails with permission errors

**Symptoms:**
- Permission denied errors during installation
- Cannot write to system directories

**Solutions:**
1. **Use virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **User installation:**
   ```bash
   pip install --user -r requirements.txt
   ```

3. **Fix permissions (Linux/Mac):**
   ```bash
   sudo chown -R $USER ~/.local/lib/python*
   ```

### Configuration Issues

#### Issue: `Config file not found` or invalid YAML

**Symptoms:**
- Error loading configuration file
- YAML parsing errors

**Solutions:**
1. **Copy example configuration:**
   ```bash
   cp config.yaml.example config.yaml
   ```

2. **Validate YAML syntax:**
   ```bash
   python -c "import yaml; yaml.safe_load(open('config.yaml'))"
   ```

3. **Check file permissions:**
   ```bash
   ls -la config.yaml
   chmod 644 config.yaml
   ```

4. **Use absolute paths:**
   ```bash
   ai-shell --config /full/path/to/config.yaml
   ```

#### Issue: API key not working

**Symptoms:**
- Authentication errors with Gemini API
- "Invalid API key" messages

**Solutions:**
1. **Verify API key format:**
   ```bash
   echo $GEMINI_API_KEY | wc -c  # Should be 39 characters
   ```

2. **Set environment variable:**
   ```bash
   export GEMINI_API_KEY="your_actual_key_here"
   # Add to ~/.bashrc or ~/.zshrc for persistence
   ```

3. **Check API key in config:**
   ```yaml
   llm:
     gemini:
       api_key: "your_key_here"  # Remove any extra spaces/quotes
   ```

4. **Test API access:**
   ```bash
   curl -H "Authorization: Bearer $GEMINI_API_KEY" \
        https://generativelanguage.googleapis.com/v1/models
   ```

### LLM Provider Issues

#### Issue: Ollama connection failed

**Symptoms:**
- "Connection refused" to localhost:11434
- Ollama provider not available

**Solutions:**
1. **Check if Ollama is running:**
   ```bash
   curl http://localhost:11434/api/version
   ```

2. **Start Ollama service:**
   ```bash
   # Linux/Mac
   ollama serve
   
   # Or as background service
   nohup ollama serve > ollama.log 2>&1 &
   ```

3. **Verify model is available:**
   ```bash
   ollama list
   ollama pull llama3  # If model not found
   ```

4. **Check configuration:**
   ```yaml
   llm:
     local:
       host: localhost
       port: 11434
       model: llama3  # Must match installed model
   ```

#### Issue: Slow response times

**Symptoms:**
- Long delays waiting for AI responses
- Timeouts or connection errors

**Solutions:**
1. **For Gemini API:**
   - Check internet connection
   - Verify API quotas and limits
   - Use smaller models (gemini-1.5-flash vs gemini-1.5-pro)

2. **For local LLMs:**
   ```bash
   # Check system resources
   htop
   nvidia-smi  # If using GPU
   
   # Use smaller models
   ollama pull llama3:8b  # Instead of llama3:70b
   ```

3. **Optimize configuration:**
   ```yaml
   llm:
     gemini:
       model: gemini-1.5-flash  # Faster than pro
   ```

### Security and Permissions

#### Issue: Commands not executing

**Symptoms:**
- AI generates commands but they don't run
- Permission denied errors

**Solutions:**
1. **Check confirmation settings:**
   ```yaml
   security:
     require_confirmation: true  # Set to false for auto-execution
   ```

2. **Verify command permissions:**
   ```bash
   # Test the generated command manually
   ls -la /path/to/file
   ```

3. **Check dangerous command list:**
   ```yaml
   security:
     dangerous_commands:
       - rm -rf  # Remove if you want to allow
   ```

#### Issue: "Command blocked by security policy"

**Symptoms:**
- Security warnings for safe commands
- Overly restrictive validation

**Solutions:**
1. **Review dangerous commands list:**
   ```yaml
   security:
     dangerous_commands:
       - rm -rf
       - format
       - dd if=
       # Remove entries you trust
   ```

2. **Disable confirmation temporarily:**
   ```bash
   ai-shell --no-confirmation
   ```

3. **Use override flag:**
   ```yaml
   security:
     require_confirmation: false
   ```

### Platform-Specific Issues

#### Windows Issues

**PowerShell execution policy:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Path issues:**
```cmd
# Add Python Scripts to PATH
set PATH=%PATH%;%USERPROFILE%\AppData\Local\Programs\Python\Python3X\Scripts
```

**Colors not working:**
```bash
# Enable ANSI colors in Windows Terminal
pip install colorama
```

#### macOS Issues

**Homebrew Python conflicts:**
```bash
# Use system Python or pyenv
pyenv install 3.11.0
pyenv global 3.11.0
```

**Permission issues:**
```bash
# Fix Homebrew permissions
sudo chown -R $(whoami) /usr/local/Homebrew
```

#### Linux Issues

**Missing dependencies:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-pip python3-venv

# CentOS/RHEL
sudo yum install python3-pip python3-venv
```

## 🔧 Debugging Tips

### Enable Debug Logging

1. **Command line:**
   ```bash
   ai-shell --log-level DEBUG
   ```

2. **Configuration file:**
   ```yaml
   logging:
     level: DEBUG
     file: debug.log
   ```

3. **View logs:**
   ```bash
   tail -f ai_shell.log
   # Or
   tail -f debug.log
   ```

### Test Components Individually

1. **Test configuration:**
   ```python
   from ai_shell.config import get_config
   config = get_config()
   print(config.get('llm.provider'))
   ```

2. **Test LLM provider:**
   ```python
   from ai_shell.llm import get_llm_provider
   from ai_shell.config import get_config
   
   config = get_config()
   provider = get_llm_provider('gemini', config)
   print(provider.is_available())
   ```

3. **Test command execution:**
   ```python
   from ai_shell.executor import get_executor
   from ai_shell.config import get_config
   
   config = get_config()
   executor = get_executor(config)
   result = executor.validate_command('ls -la')
   print(result)
   ```

### Network Debugging

1. **Test API connectivity:**
   ```bash
   # Test Gemini API
   curl -H "Authorization: Bearer $GEMINI_API_KEY" \
        https://generativelanguage.googleapis.com/v1/models
   
   # Test Ollama
   curl http://localhost:11434/api/version
   ```

2. **Check proxy settings:**
   ```bash
   echo $HTTP_PROXY
   echo $HTTPS_PROXY
   ```

3. **Bypass proxy for local connections:**
   ```bash
   export NO_PROXY=localhost,127.0.0.1
   ```

## 📊 Performance Tuning

### System Requirements

**Minimum:**
- Python 3.8+
- 4GB RAM
- 1GB free disk space

**Recommended:**
- Python 3.11+
- 8GB RAM
- 5GB free disk space
- SSD storage

### Optimization Tips

1. **For local LLMs:**
   ```bash
   # Use quantized models
   ollama pull llama3:8b-q4_0
   
   # Monitor resource usage
   htop
   nvidia-smi  # For GPU
   ```

2. **For API-based LLMs:**
   ```yaml
   # Use faster models
   llm:
     gemini:
       model: gemini-1.5-flash
   ```

3. **Reduce logging:**
   ```yaml
   logging:
     level: WARNING  # Instead of DEBUG/INFO
   ```

## 🆘 Getting Help

### Before Asking for Help

1. **Search existing issues:**
   - [GitHub Issues](https://github.com/GizzZmo/Ai_shell/issues)
   - [GitHub Discussions](https://github.com/GizzZmo/Ai_shell/discussions)

2. **Check documentation:**
   - README.md
   - This troubleshooting guide
   - Architecture documentation

3. **Gather information:**
   ```bash
   # System information
   uname -a
   python --version
   pip list | grep -E "(ai-shell|google-generativeai|requests)"
   
   # AI Shell version
   ai-shell --version
   
   # Configuration
   cat config.yaml
   ```

### Reporting Issues

**Include this information:**
- Operating system and version
- Python version
- AI Shell version
- Configuration file (remove API keys)
- Full error message and stack trace
- Steps to reproduce the issue

**Issue template:**
```markdown
## Environment
- OS: [e.g., Ubuntu 22.04, Windows 11, macOS 13.0]
- Python: [e.g., 3.11.0]
- AI Shell: [e.g., 0.1.0]

## Configuration
```yaml
# Your config.yaml (remove API keys)
```

## Issue Description
[Clear description of the problem]

## Steps to Reproduce
1. Run command X
2. See error Y

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Error Messages
```
[Full error message and stack trace]
```

## Additional Context
[Any other relevant information]
```

### Community Support

- **GitHub Discussions**: General questions and community help
- **GitHub Issues**: Bug reports and feature requests
- **Code Review**: Learning and improvement opportunities

Remember: The more detailed information you provide, the easier it is for others to help you! 🚀