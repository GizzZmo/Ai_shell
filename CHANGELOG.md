# Changelog

All notable changes to AI Shell will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation rewrite
- Enhanced CONTRIBUTING.md with detailed development guidelines
- CHANGELOG.md for tracking version history

### Changed
- README.md completely restructured for better user experience
- Improved documentation organization and clarity

### Security
- Documentation of security features and best practices

## [0.1.0] - Current Release

### Added
- Multi-modal architecture with three operating modes:
  - Command Translator: Direct natural language to command translation
  - AI Assistant: Conversational mode with chat history
  - Metasploit Assistant: Specialized penetration testing support
- LLM provider support:
  - Google Gemini integration
  - Local LLM support via Ollama
- Interactive tool integration using pseudoterminal (pty)
- Real-time command output streaming
- Security features:
  - Command validation and dangerous command detection
  - User confirmation before command execution
  - Input sanitization
- Configuration management with YAML support
- Training data collection with feedback loop
- Comprehensive test suite
- Cross-platform installation scripts (Windows/Linux/Mac)

### Changed
- Evolved from simple translator (v0.0.3) to multi-tool platform
- Enhanced UI with better colors and user experience
- Improved error handling and logging

### Security
- Built-in command validation system
- Configurable dangerous command lists
- User confirmation requirements

## [0.0.3] - Legacy Version

### Added
- Basic command translation functionality
- Simple subprocess-based command execution
- Initial LLM integration

### Notes
- This version served as the foundation for the current multi-modal architecture
- Deprecated in favor of the enhanced v0.1.0 architecture

---

## Release Guidelines

### Version Numbers
- **MAJOR**: Breaking changes to API or core functionality
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Release Process
1. Update CHANGELOG.md with new version
2. Update version in setup.py and __init__.py
3. Create git tag with version number
4. Generate release notes from changelog
5. Publish to PyPI (when ready)

### Categories
- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Features that will be removed
- **Removed**: Features that have been removed
- **Fixed**: Bug fixes
- **Security**: Security-related changes