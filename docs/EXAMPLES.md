# Examples and Tutorials

This guide provides practical examples and step-by-step tutorials for using AI Shell effectively.

## 🚀 Quick Start Examples

### Basic Command Translation

Transform natural language into shell commands:

```bash
# Start AI Shell in translator mode
ai-shell --mode translator

# Example interactions:
> find all Python files in my current directory
→ find . -name "*.py" -type f

> show me the largest files in my home directory
→ find ~ -type f -exec ls -lah {} + | sort -k5 -hr | head -10

> compress all log files older than 7 days
→ find /var/log -name "*.log" -mtime +7 -exec gzip {} \;

> show running processes sorted by memory usage
→ ps aux --sort=-%mem | head -20
```
Assistant: I'll help you set up a Python virtual environment. Here's a step-by-step process:

1. **Create the virtual environment:**
   ```bash
   python -m venv myproject_env
   ```

2. **Activate the environment:**
   ```bash
   source myproject_env/bin/activate  # On Windows: myproject_env\Scripts\activate
   ```

3. **Verify activation:**
   ```bash
   which python  # Should show the venv path
   ```

4. **Install packages:**
   ```bash
   pip install requests flask  # Example packages
   ```

5. **Create requirements file:**
Assistant: Simply run the `deactivate` command:

```bash
deactivate
```

This will return you to your system's default Python environment. The environment will remain intact and you can reactivate it anytime with the activation command.
```

### Metasploit Assistant

Security testing with AI guidance:

```bash
# Start Metasploit mode
Assistant: I can help you find SMB vulnerabilities. Try this search command:

```bash
search type:exploit platform:windows service:smb
```

Assistant: To set up a listener for a reverse shell, use the multi/handler module:

```bash
use exploit/multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST your_ip_address
set LPORT 4444
run
```

This creates a listener on port 4444 that will catch reverse connections.
```

## 📚 Detailed Tutorials
Assistant: I'll help you organize photos by date. Here's a systematic approach:

1. **Find all image files:**
   ```bash
   find . -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.gif" \) > photo_list.txt
   ```

2. **Create date-based directories:**
   ```bash
   # This script creates folders and moves files by date
   for file in $(cat photo_list.txt); do
     date=$(stat -c %y "$file" | cut -d' ' -f1)
     year=$(echo $date | cut -d'-' -f1)
     month=$(echo $date | cut -d'-' -f2)
     mkdir -p "Photos/$year/$month"
     mv "$file" "Photos/$year/$month/"
   done
   ```

3. **Verify organization:**
   ```bash
   tree Photos/
   ```

Would you like me to explain how to handle duplicates or add more organization criteria?
→ cat > monitor.sh << 'EOF'
#!/bin/bash
while true; do
  echo "$(date): CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}'), Memory: $(free | grep Mem | awk '{printf "%.1f%%", $3/$2 * 100.0}'), Disk: $(df -h / | awk 'NR==2{print $5}')" >> system_monitor.log
  sleep 300
done
EOF
→ sudo tee /etc/logrotate.d/system_monitor << 'EOF'
/path/to/system_monitor.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
EOF

### Tutorial 3: Development Environment Setup

Quickly set up development environments:
Assistant: I'll help you set up a complete Node.js + TypeScript development environment:

1. **Initialize the project:**
   ```bash
   mkdir my-typescript-project && cd my-typescript-project
   npm init -y
   ```

2. **Install TypeScript and development dependencies:**
   ```bash
   npm install -D typescript @types/node ts-node nodemon
   npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
   npm install -D prettier eslint-config-prettier eslint-plugin-prettier
   ```

3. **Create TypeScript configuration:**
   ```bash
   npx tsc --init
   ```

4. **Set up ESLint configuration:**
   ```bash
   cat > .eslintrc.js << 'EOF'
   module.exports = {
     parser: '@typescript-eslint/parser',
     extends: [
       '@typescript-eslint/recommended',
       'prettier'
     ],
     plugins: ['@typescript-eslint', 'prettier'],
     rules: {
       'prettier/prettier': 'error'
     }
   };
   EOF
   ```

5. **Create Prettier configuration:**
   ```bash
   echo '{"semi": true, "singleQuote": true, "tabWidth": 2}' > .prettierrc
   ```

6. **Add scripts to package.json:**
   ```bash
   npm pkg set scripts.start="node dist/index.js"
   npm pkg set scripts.dev="nodemon --exec ts-node src/index.ts"
   npm pkg set scripts.build="tsc"
   npm pkg set scripts.lint="eslint src/**/*.ts"
   npm pkg set scripts.format="prettier --write src/**/*.ts"
   ```

Your development environment is ready! Create `src/index.ts` and start coding.

## 🔧 Advanced Use Cases

### Custom Configuration Examples

**Multiple API Keys Setup:**
```yaml
# config.yaml
llm:
  provider: gemini
  gemini:
    api_key: !ENV ${GEMINI_API_KEY}
    model: gemini-1.5-flash
    backup_key: !ENV ${GEMINI_BACKUP_KEY}
  
  local:
    host: localhost
    port: 11434
    models:
      - llama3:8b
      - codellama:13b
      - mistral:7b
```

**Security Customization:**
```yaml
security:
  require_confirmation: true
  dangerous_commands:
    - rm -rf
    - sudo rm
    - format
    - mkfs
    - dd if=
  safe_commands:
    - ls
    - cat
    - grep
    - find
  custom_validators:
    - no_system_dirs: true
    - max_file_size: 1GB
```

### Automation Scripts

**Daily System Cleanup:**
```bash
#!/bin/bash
# daily_cleanup.sh - Use AI Shell for maintenance tasks

# Clean temporary files
ai-shell --mode translator --no-confirmation << 'EOF'
remove all files in /tmp older than 3 days
clear package manager cache
find and remove duplicate files in Downloads folder
EOF

# System updates
ai-shell --mode assistant << 'EOF'
Guide me through updating system packages safely
EOF
```

**Development Workflow:**
```bash
#!/bin/bash
# dev_workflow.sh - Automated development tasks

PROJECT_DIR=$1
cd "$PROJECT_DIR"

# Use AI Shell for code maintenance
ai-shell --mode translator --no-confirmation << 'EOF'
run linting on all Python files and fix auto-fixable issues
update requirements.txt with current dependencies
run tests and generate coverage report
check for security vulnerabilities in dependencies
EOF
```

### Integration Examples

**Git Workflow Integration:**
```bash
# .git/hooks/pre-commit
#!/bin/bash
# Use AI Shell for intelligent pre-commit checks

ai-shell --mode assistant --no-confirmation << 'EOF'
Analyze the staged changes and suggest any improvements
Check for potential security issues in the code
Verify that tests exist for new functionality
EOF
```

**CI/CD Pipeline Enhancement:**
```yaml
# .github/workflows/ai-assisted-review.yml
name: AI-Assisted Code Review

on: [pull_request]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: AI Code Review
        run: |
          ai-shell --mode assistant << 'EOF'
          Review the code changes in this PR for:
          1. Code quality and best practices
          2. Potential bugs or security issues
          3. Performance optimizations
          4. Documentation completeness
          EOF
```

## 🎯 Best Practices

### Effective Prompting

**Good Prompts:**
- "Find all Python files modified in the last week"
- "Show me processes using more than 1GB of memory"
- "Create a backup of the database with timestamp"
- "Set up a simple HTTP server on port 8000"

**Avoid Vague Prompts:**
- "Fix my computer"
- "Make it faster"
- "Clean everything"
- "Install stuff"

### Security Guidelines

1. **Always review commands before execution**
2. **Use confirmation mode in production environments**
3. **Regularly audit dangerous command lists**
4. **Keep API keys secure and rotate them regularly**
5. **Monitor command logs for unusual activity**

### Performance Optimization

1. **Use local LLMs for sensitive data**
2. **Cache common responses**
3. **Optimize prompt length**
4. **Use appropriate models for the task**

## 🚀 Next Steps

After mastering these examples:

1. **Explore Advanced Features:**
   - Custom system prompts
   - Plugin development
   - API integrations

2. **Contribute to the Project:**
   - Report bugs and suggest features
   - Contribute new examples
   - Improve documentation

3. **Share Your Use Cases:**
   - Create tutorials for your domain
   - Share automation scripts
   - Help other users

Remember: AI Shell learns from your usage patterns. The more you use it, the better it becomes at understanding your preferences and workflow!

For more advanced topics, see:
- [Architecture Documentation](ARCHITECTURE.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)
- [Contributing Guidelines](../CONTRIBUTING.md)

```bash
ai-shell --mode assistant

You: I want to set up a new Node.js project with TypeScript, ESLint, and Prettier
chmod +x monitor.sh

# Set up log rotation
> configure logrotate for the monitoring log to prevent it from growing too large

### Tutorial 2: System Monitoring Setup

Set up comprehensive system monitoring:

```bash
# Start translator mode for quick commands
ai-shell --mode translator

# Monitor system resources
> create a script to monitor CPU, memory, and disk usage every 5 minutes

### Tutorial 1: File Management Tasks

Learn to use AI Shell for common file operations:

```bash
# Start AI Shell
ai-shell --mode assistant

# Find and organize files
You: I have photos scattered in different folders. How can I organize them by date?
This will show exploits targeting Windows SMB services. Would you like me to explain any specific exploits?

? how do I set up a listener for a reverse shell
ai-shell --mode metasploit

# Direct msfconsole commands work normally:
msf6 > workspace -a test_project
msf6 > hosts

# Use '?' prefix for AI assistance:
? search for vulnerabilities in Windows SMB services
   ```bash
   pip freeze > requirements.txt
   ```

Would you like me to explain any of these steps in more detail?

You: How do I deactivate the environment when I'm done?


### Conversational Assistant

Get explanations and multi-step guidance:

```bash
# Start in assistant mode
ai-shell --mode assistant

# Example conversation:
You: I need to set up a Python virtual environment for a new project