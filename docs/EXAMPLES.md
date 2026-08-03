# Examples and Tutorials

This guide provides practical examples and step-by-step tutorials for using AI Shell effectively.

## Quick Start Examples

### Basic Command Translation

Start AI Shell in translator mode and enter natural language prompts:

```bash
ai-shell --mode translator
```

Example interactions:

```
> find all Python files in my current directory
-> find . -name "*.py" -type f

> show me the largest files in my home directory
-> find ~ -type f -exec ls -lah {} + | sort -k5 -hr | head -10

> compress all log files older than 7 days
-> find /var/log -name "*.log" -mtime +7 -exec gzip {} \;

> show running processes sorted by memory usage
-> ps aux --sort=-%mem | head -20

> count lines of code in all Python files recursively
-> find . -name "*.py" | xargs wc -l | tail -1
```

### Conversational Assistant

Start in assistant mode for multi-turn conversations with context memory:

```bash
ai-shell --mode assistant
```

Example conversation:

```
You: I need to set up a Python virtual environment for a new project

Assistant: Here is how to create and activate a virtual environment:

1. Create the environment:
   python -m venv myproject_env

2. Activate it:
   source myproject_env/bin/activate   # Linux/Mac
   myproject_env\Scripts\activate     # Windows

3. Install packages:
   pip install requests flask

4. Save dependencies:
   pip freeze > requirements.txt

You: How do I deactivate when I'm done?

Assistant: Simply run:
   deactivate

This returns you to your system Python. The environment is preserved and
can be re-activated any time with the activation command above.
```

### Metasploit Assistant

Security testing with AI guidance inside a live `msfconsole` session:

```bash
ai-shell --mode metasploit
```

Once `msfconsole` opens, regular commands work as usual. Prefix a line with `?` to ask the AI:

```
? search for vulnerabilities in Windows SMB services

Assistant: I can help you find SMB vulnerabilities. Try:
   search type:exploit platform:windows service:smb

? set up a listener for a reverse shell

Assistant: Use the multi/handler module:
   use exploit/multi/handler
   set PAYLOAD windows/meterpreter/reverse_tcp
   set LHOST your_ip_address
   set LPORT 4444
   run
```

### Wapiti Assistant

Web application scanning with AI guidance:

```bash
ai-shell --mode wapiti
```

A Bash shell opens. Use `?` to get wapiti commands from the AI:

```
? scan http://testphp.vulnweb.com for XSS and SQL injection

Assistant: To scan for both XSS and SQLi vulnerabilities:
   wapiti -u http://testphp.vulnweb.com -m xss,sql --scope domain

? run a quick scan of example.com

Assistant: For a quick scan:
   wapiti -u http://example.com
```

---

## Detailed Tutorials

### Tutorial 1: File Management Tasks

Learn to use AI Shell for common file operations:

```bash
ai-shell --mode assistant
```

```
You: I have photos scattered in different folders. How can I organize them by date?

Assistant: Here is a script to organize photos by year and month based on file modification date:

   find . -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | while read file; do
     date=$(stat -c %y "$file" | cut -d" " -f1)
     year=$(echo $date | cut -d"-" -f1)
     month=$(echo $date | cut -d"-" -f2)
     mkdir -p "Photos/$year/$month"
     mv "$file" "Photos/$year/$month/"
   done

You: How do I verify the result?

Assistant: Use the tree command:
   tree Photos/
```

### Tutorial 2: System Monitoring Setup

Set up comprehensive system monitoring:

```bash
ai-shell --mode translator
```

```
> create a script to monitor CPU, memory, and disk usage every 5 minutes
-> cat > monitor.sh << 'EOF'
   #!/bin/bash
   while true; do
     echo "$(date): CPU: $(top -bn1 | grep Cpu | awk "{print \$2}"), \
       Mem: $(free | grep Mem | awk "{printf \"%.1f%%\", \$3/\$2*100}")" >> system_monitor.log
     sleep 300
   done
   EOF
   chmod +x monitor.sh
```

### Tutorial 3: Development Environment Setup

Quickly set up development environments:

```bash
ai-shell --mode assistant
```

```
You: Set up a Node.js + TypeScript project with ESLint and Prettier

Assistant: Here are the steps:

1. Initialize the project:
   mkdir my-ts-project && cd my-ts-project
   npm init -y

2. Install TypeScript and tooling:
   npm install -D typescript @types/node ts-node nodemon
   npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
   npm install -D prettier eslint-config-prettier

3. Create TypeScript config:
   npx tsc --init

4. Add scripts to package.json:
   npm pkg set scripts.dev="nodemon --exec ts-node src/index.ts"
   npm pkg set scripts.build="tsc"
   npm pkg set scripts.lint="eslint src"

Create src/index.ts and start coding!
```

---

## Advanced Use Cases

### Automation Scripts

**Daily System Cleanup:**

```bash
#!/bin/bash
# daily_cleanup.sh - Use AI Shell for maintenance tasks

# Clean temporary files
ai-shell --mode translator --no-confirmation <<'INPUT'
remove all files in /tmp older than 3 days
INPUT
```

**Development Workflow:**

```bash
#!/bin/bash
# dev_workflow.sh

PROJECT_DIR=$1
cd "$PROJECT_DIR"

ai-shell --mode translator --no-confirmation <<'INPUT'
run linting on all Python files
update requirements.txt with current dependencies
run tests and generate coverage report
INPUT
```

### Custom Configuration Examples

**Minimal Gemini config:**

```yaml
llm:
  provider: gemini
  gemini:
    api_key: ""  # or set GEMINI_API_KEY env var
    model: gemini-1.5-flash
```

**Local LLM config:**

```yaml
llm:
  provider: local
  local:
    host: localhost
    port: 11434
    model: llama3
```

**Strict security config:**

```yaml
security:
  require_confirmation: true
  dangerous_commands:
    - rm -rf
    - format
    - dd if=
    - mkfs
    - fdisk
    - wipefs
    - shred
    - chmod 777
```

---

## Best Practices

### Effective Prompting

**Good prompts (specific and actionable):**
- "Find all Python files modified in the last week"
- "Show me processes using more than 1 GB of memory"
- "Create a gzip backup of the database with a timestamp in the filename"
- "Set up a simple HTTP server on port 8000 in the current directory"

**Avoid vague prompts:**
- "Fix my computer"
- "Make it faster"
- "Clean everything"
- "Install stuff"

### Security Guidelines

1. **Always review commands before execution** — read every command the AI proposes
2. **Use confirmation mode in production** — do not use `--no-confirmation` on live systems
3. **Audit the dangerous commands list** — customise `security.dangerous_commands` in `config.yaml`
4. **Keep API keys secure** — use environment variables; never store them in config files checked into git
5. **Only scan systems you own or have permission to test** — especially in Metasploit and Wapiti modes

### Performance Tips

1. **Use local LLMs for sensitive data** — prevents sending data to external APIs
2. **Choose the right model size** — `llama3:8b` is much faster than `:70b` for simple tasks
3. **Use `gemini-1.5-flash`** — faster and cheaper than `gemini-1.5-pro` for most tasks
4. **Reduce log verbosity** — set `logging.level: WARNING` once the setup is stable

---

For more advanced topics, see:
- [Architecture Documentation](ARCHITECTURE.md)
- [Configuration Guide](CONFIGURATION.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)
- [Contributing Guidelines](../CONTRIBUTING.md)
