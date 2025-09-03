# Configuration Guide

This guide provides comprehensive information about configuring AI Shell for optimal performance and security.

## 📋 Configuration Overview

AI Shell uses a YAML-based configuration system with support for environment variables and default fallbacks. The configuration controls LLM providers, security settings, logging, and training data collection.

### Configuration Hierarchy

1. **Command-line arguments** (highest priority)
2. **Environment variables**
3. **Configuration file** (`config.yaml`)
4. **Default values** (lowest priority)

## 🔧 Basic Configuration

### Creating Your First Config

```bash
# Copy the example configuration
cp config.yaml.example config.yaml

# Edit with your preferred editor
nano config.yaml
```

### Minimal Configuration

```yaml
# Minimal config for Gemini API
llm:
  provider: gemini
  gemini:
    api_key: "your_gemini_api_key_here"
```

```yaml
# Minimal config for local LLM
llm:
  provider: local
  local:
    model: llama3
```

## 🧠 LLM Provider Configuration

### Google Gemini

```yaml
llm:
  provider: gemini
  gemini:
    api_key: ""  # Your API key or use GEMINI_API_KEY env var
    model: gemini-1.5-flash  # Options: gemini-1.5-flash, gemini-1.5-pro
    temperature: 0.1  # Controls randomness (0.0-2.0)
    max_tokens: 2048  # Maximum response length
    timeout: 30  # Request timeout in seconds
```

**Environment Variables:**
```bash
export GEMINI_API_KEY="your_key_here"
export GEMINI_MODEL="gemini-1.5-flash"
```

**Available Models:**
- `gemini-1.5-flash`: Fast, cost-effective for most tasks
- `gemini-1.5-pro`: More capable, higher cost
- `gemini-1.0-pro`: Legacy model

### Local LLM (Ollama)

```yaml
llm:
  provider: local
  local:
    host: localhost
    port: 11434
    model: llama3  # Must be installed via 'ollama pull'
    temperature: 0.1
    max_tokens: 2048
    timeout: 60  # Local models may need more time
    context_window: 4096  # Model context size
```

**Advanced Local Configuration:**
```yaml
llm:
  provider: local
  local:
    host: localhost
    port: 11434
    models:
      default: llama3:8b
      code: codellama:13b
      security: llama3:70b
    model_selection: auto  # or 'manual'
    gpu_layers: -1  # Use all GPU layers
    num_thread: 8  # CPU threads to use
```

**Supported Local Models:**
- `llama3:8b` - General purpose, good balance
- `llama3:70b` - Most capable, requires more resources
- `codellama:13b` - Optimized for code generation
- `mistral:7b` - Fast and efficient
- `mixtral:8x7b` - Mixture of experts model

## 🔒 Security Configuration

### Basic Security Settings

```yaml
security:
  require_confirmation: true  # Always ask before executing commands
  dangerous_commands:
    - rm -rf
    - format
    - dd if=
    - mkfs
    - fdisk
    - wipefs
    - shred
    - chmod 777
    - chown -R root
  
  # Commands that bypass confirmation
  safe_commands:
    - ls
    - cat
    - echo
    - pwd
    - whoami
    - date
```

### Advanced Security Configuration

```yaml
security:
  require_confirmation: true
  
  # Command validation rules
  validation:
    max_command_length: 1000
    allow_pipes: true
    allow_redirects: true
    block_privilege_escalation: true
    
  # Path restrictions
  restricted_paths:
    - /etc/passwd
    - /etc/shadow
    - /boot
    - /sys
    - /proc/*/mem
  
  # User restrictions
  allowed_users:
    - myuser
    - developer
  
  # Environment restrictions
  blocked_env_vars:
    - LD_PRELOAD
    - DYLD_INSERT_LIBRARIES
  
  # Audit settings
  audit_log: true
  audit_file: /var/log/ai_shell_audit.log
```

### Security Profiles

**Development Profile:**
```yaml
security:
  require_confirmation: false
  dangerous_commands: []  # Allow everything for development
  audit_log: true
```

**Production Profile:**
```yaml
security:
  require_confirmation: true
  dangerous_commands:
    - rm -rf
    - sudo
    - chmod
    - chown
    - mount
    - umount
  strict_mode: true
  audit_log: true
```

**High-Security Profile:**
```yaml
security:
  require_confirmation: true
  dangerous_commands:
    - rm
    - mv
    - cp
    - chmod
    - chown
    - sudo
    - su
  whitelist_mode: true  # Only allow explicitly safe commands
  safe_commands:
    - ls
    - cat
    - grep
    - find
    - head
    - tail
```

## 📊 Logging Configuration

### Basic Logging

```yaml
logging:
  level: INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
  file: ai_shell.log
  format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
```

### Advanced Logging

```yaml
logging:
  level: INFO
  
  # Multiple log handlers
  handlers:
    file:
      filename: ai_shell.log
      max_bytes: 10485760  # 10MB
      backup_count: 5
      format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    console:
      level: WARNING
      format: '%(levelname)s: %(message)s'
    
    syslog:
      address: localhost:514
      facility: user
      format: 'ai_shell[%(process)d]: %(message)s'
  
  # Component-specific logging
  loggers:
    ai_shell.llm: DEBUG
    ai_shell.executor: INFO
    ai_shell.security: WARNING
```

### Log Rotation

```yaml
logging:
  file: ai_shell.log
  rotation:
    max_size: 50MB
    backup_count: 10
    compress: true
    when: midnight  # Daily rotation
```

## 📈 Training Configuration

### Basic Training Settings

```yaml
training:
  dataset_file: training_dataset.jsonl
  auto_log: true  # Automatically log successful commands
  include_corrections: true  # Log user corrections
```

### Advanced Training Configuration

```yaml
training:
  dataset_file: training_dataset.jsonl
  auto_log: true
  
  # Data collection settings
  collection:
    include_system_info: false  # Don't log system details
    anonymize_paths: true  # Replace /home/user with /home/[USER]
    include_timestamps: true
    include_execution_time: true
  
  # Quality filters
  filters:
    min_command_length: 3
    max_command_length: 200
    exclude_failed_commands: true
    exclude_dangerous_commands: true
  
  # Export settings
  export:
    format: jsonl  # or 'csv', 'json'
    batch_size: 1000
    compression: gzip
```

## 🌍 Environment Variables

### Core Environment Variables

```bash
# LLM Configuration
export GEMINI_API_KEY="your_key_here"
export AI_SHELL_CONFIG="/path/to/config.yaml"
export AI_SHELL_PROVIDER="local"  # or "gemini"

# Security
export AI_SHELL_CONFIRM="true"  # Require confirmation
export AI_SHELL_SAFE_MODE="true"  # Extra security checks

# Logging
export AI_SHELL_LOG_LEVEL="DEBUG"
export AI_SHELL_LOG_FILE="/var/log/ai_shell.log"

# Training
export AI_SHELL_TRAINING_FILE="/path/to/training.jsonl"
export AI_SHELL_AUTO_LOG="true"
```

### Provider-Specific Variables

**Gemini:**
```bash
export GEMINI_API_KEY="your_key"
export GEMINI_MODEL="gemini-1.5-flash"
export GEMINI_TEMPERATURE="0.1"
export GEMINI_TIMEOUT="30"
```

**Ollama:**
```bash
export OLLAMA_HOST="localhost"
export OLLAMA_PORT="11434"
export OLLAMA_MODEL="llama3"
export OLLAMA_GPU_LAYERS="-1"
export OLLAMA_NUM_THREAD="8"
```

## 🔧 Advanced Configuration

### Multiple Profiles

Create different configurations for different contexts:

**Profile Structure:**
```
~/.ai_shell/
├── config/
│   ├── development.yaml
│   ├── production.yaml
│   ├── security_testing.yaml
│   └── default.yaml
└── profiles/
    ├── work.yaml
    └── personal.yaml
```

**Using Profiles:**
```bash
ai-shell --config ~/.ai_shell/config/development.yaml
ai-shell --profile work
```

### Dynamic Configuration

```yaml
# config.yaml with dynamic elements
llm:
  provider: !ENV ${AI_SHELL_PROVIDER:gemini}  # Default to gemini
  gemini:
    api_key: !ENV ${GEMINI_API_KEY}
    model: !ENV ${GEMINI_MODEL:gemini-1.5-flash}
  
security:
  require_confirmation: !ENV ${AI_SHELL_CONFIRM:true}
  dangerous_commands: !INCLUDE dangerous_commands.yaml

logging:
  level: !ENV ${LOG_LEVEL:INFO}
  file: !ENV ${LOG_FILE:ai_shell.log}
```

### Configuration Validation

AI Shell validates your configuration on startup:

```bash
# Test configuration
ai-shell --config config.yaml --validate-config

# Show effective configuration
ai-shell --show-config
```

**Common Validation Errors:**
- Missing required API keys
- Invalid model names
- Malformed YAML syntax
- Conflicting security settings

## 🎨 UI Configuration

### Terminal Appearance

```yaml
ui:
  colors:
    primary: cyan
    secondary: magenta
    success: green
    warning: yellow
    error: red
    info: blue
  
  formatting:
    banner: true
    timestamps: true
    command_highlighting: true
    progress_bars: true
  
  terminal:
    width: auto  # or specific number
    pager: less
    editor: nano  # or vim, emacs, code
```

### Output Formatting

```yaml
ui:
  output:
    stream_commands: true  # Show output in real-time
    buffer_size: 4096
    max_lines: 1000
    truncate_long_output: true
    
  prompts:
    show_mode: true
    show_provider: true
    custom_prompt: "AI> "
    
  notifications:
    sound: false
    desktop: true  # Desktop notifications
```

## 🔍 Debugging Configuration

### Debug Mode

```yaml
debug:
  enabled: true
  verbose: true
  save_requests: true
  save_responses: true
  request_file: debug_requests.json
  response_file: debug_responses.json
  
  # Performance monitoring
  profile: true
  timing: true
  memory_usage: true
```

### Troubleshooting Configuration

```bash
# Enable maximum debugging
export AI_SHELL_DEBUG=1
export AI_SHELL_VERBOSE=1
ai-shell --log-level DEBUG

# Test specific components
ai-shell --test-llm
ai-shell --test-config
ai-shell --test-security
```

## 📝 Configuration Templates

### Basic User Template

```yaml
# ~/.ai_shell/config.yaml
llm:
  provider: gemini
  gemini:
    api_key: !ENV ${GEMINI_API_KEY}

security:
  require_confirmation: true
  
logging:
  level: INFO
  file: ~/.ai_shell/ai_shell.log
```

### Power User Template

```yaml
llm:
  provider: local
  local:
    host: localhost
    port: 11434
    model: llama3:70b
    
security:
  require_confirmation: false
  dangerous_commands:
    - rm -rf /
    - format
    
logging:
  level: DEBUG
  handlers:
    file:
      filename: ~/.ai_shell/debug.log
    console:
      level: WARNING
      
training:
  auto_log: true
  dataset_file: ~/.ai_shell/training.jsonl
```

### Enterprise Template

```yaml
llm:
  provider: local  # Keep data on-premises
  local:
    host: llm-server.company.com
    port: 11434
    model: llama3:70b
    
security:
  require_confirmation: true
  audit_log: true
  audit_file: /var/log/ai_shell_audit.log
  
  dangerous_commands:
    - rm
    - mv
    - chmod
    - chown
    - sudo
    - mount
    - systemctl
    
logging:
  level: INFO
  handlers:
    syslog:
      address: syslog.company.com:514
      facility: user
      
training:
  auto_log: false  # Manual approval only
```

## 🚀 Best Practices

### Security Best Practices

1. **Never commit API keys to version control**
2. **Use environment variables for sensitive data**
3. **Regularly rotate API keys**
4. **Enable audit logging in production**
5. **Use least-privilege security profiles**

### Performance Best Practices

1. **Use appropriate models for the task**
2. **Configure reasonable timeouts**
3. **Enable local caching when possible**
4. **Monitor resource usage**
5. **Use log rotation to prevent disk issues**

### Maintenance Best Practices

1. **Regularly review and update configurations**
2. **Test configuration changes in development first**
3. **Monitor log files for errors**
4. **Keep backup configurations**
5. **Document custom configurations**

For more detailed information, see:
- [Architecture Documentation](docs/ARCHITECTURE.md)
- [Examples and Tutorials](docs/EXAMPLES.md)
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md)