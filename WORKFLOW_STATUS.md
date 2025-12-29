# 🚀 AI Shell - Workflow Status Dashboard

*This dashboard is automatically updated by GitHub Actions*

## 📋 Workflow Status

| Workflow | Status | Description |
|----------|--------|-------------|
| **CI** | [![CI](https://github.com/GizzZmo/Ai_shell/actions/workflows/ci.yml/badge.svg)](https://github.com/GizzZmo/Ai_shell/actions/workflows/ci.yml) | Continuous integration with multi-OS and multi-Python version testing |
| **Security** | [![Security](https://github.com/GizzZmo/Ai_shell/actions/workflows/security.yml/badge.svg)](https://github.com/GizzZmo/Ai_shell/actions/workflows/security.yml) | CodeQL analysis, dependency scanning, and secrets detection |
| **Documentation** | [![Documentation](https://github.com/GizzZmo/Ai_shell/actions/workflows/documentation.yml/badge.svg)](https://github.com/GizzZmo/Ai_shell/actions/workflows/documentation.yml) | Documentation validation and GitHub Pages deployment |
| **Performance** | [![Performance](https://github.com/GizzZmo/Ai_shell/actions/workflows/performance.yml/badge.svg)](https://github.com/GizzZmo/Ai_shell/actions/workflows/performance.yml) | Benchmark tests and performance monitoring |
| **Release** | [![Release](https://github.com/GizzZmo/Ai_shell/actions/workflows/release.yml/badge.svg)](https://github.com/GizzZmo/Ai_shell/actions/workflows/release.yml) | Automated releases to GitHub and PyPI |
| **Auto Label** | [![Auto Label](https://github.com/GizzZmo/Ai_shell/actions/workflows/auto-label.yml/badge.svg)](https://github.com/GizzZmo/Ai_shell/actions/workflows/auto-label.yml) | Automatic issue and PR labeling |
| **Workflow Status** | [![Workflow Status](https://github.com/GizzZmo/Ai_shell/actions/workflows/status.yml/badge.svg)](https://github.com/GizzZmo/Ai_shell/actions/workflows/status.yml) | Generates this status dashboard |

## 📊 Repository Health

### Code Quality
- **Test Coverage**: [![Codecov](https://codecov.io/gh/GizzZmo/Ai_shell/branch/main/graph/badge.svg)](https://codecov.io/gh/GizzZmo/Ai_shell)
- **Code Security**: [![CodeQL](https://github.com/GizzZmo/Ai_shell/workflows/Security/badge.svg)](https://github.com/GizzZmo/Ai_shell/security/code-scanning)
- **License**: [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### Build Status by Platform
- **Ubuntu**: Tests run on latest Ubuntu with Python 3.9-3.12
- **Windows**: Tests run on latest Windows with Python 3.11-3.12
- **macOS**: Tests run on latest macOS with Python 3.11-3.12

## 🔄 Workflow Triggers

### Continuous Integration (CI)
- **Push**: Runs on push to `main` or `master` branches
- **Pull Request**: Runs on all PRs to `main` or `master`
- **Manual**: Can be triggered manually via workflow_dispatch

### Security
- **Push**: Runs on push to `main` or `master` branches
- **Pull Request**: Runs on all PRs to `main` or `master`
- **Schedule**: Daily at 6 AM UTC
- **Manual**: Can be triggered manually via workflow_dispatch

### Documentation
- **Push**: Runs when documentation files are modified
- **Pull Request**: Validates docs in PRs
- **Manual**: Can be triggered manually via workflow_dispatch

### Performance
- **Push**: Runs on push to `main` or `master` branches
- **Pull Request**: Runs on all PRs to `main` or `master`
- **Schedule**: Weekly on Mondays at 2 AM UTC
- **Manual**: Can be triggered manually via workflow_dispatch

### Release
- **Tag**: Runs automatically when a version tag is pushed (e.g., `v1.0.0`)
- **Manual**: Can be triggered manually with custom version input

### Auto Label
- **Issues**: Automatically labels new issues based on content
- **Pull Requests**: Automatically labels PRs based on changed files

### Workflow Status
- **Workflow Completion**: Updates after any workflow completes
- **Schedule**: Daily status report at 8 AM UTC
- **Manual**: Can be triggered manually via workflow_dispatch

## 🔗 Quick Links

- [📋 All Workflows](https://github.com/GizzZmo/Ai_shell/actions)
- [🐛 Report Issues](https://github.com/GizzZmo/Ai_shell/issues/new/choose)
- [💡 Discussions](https://github.com/GizzZmo/Ai_shell/discussions)
- [📖 Documentation](https://github.com/GizzZmo/Ai_shell/blob/main/README.md)
- [🤝 Contributing](https://github.com/GizzZmo/Ai_shell/blob/main/CONTRIBUTING.md)
- [📦 Latest Release](https://github.com/GizzZmo/Ai_shell/releases/latest)

## 📈 Workflow Details

### CI Workflow Features
- Multi-OS testing (Ubuntu, Windows, macOS)
- Multi-version Python support (3.9-3.12)
- Code linting with flake8
- Code formatting checks with black
- Comprehensive test suite with pytest
- Code coverage reporting to Codecov
- Package installation validation

### Security Workflow Features
- CodeQL static analysis with extended security queries
- Dependency vulnerability scanning with Safety
- Secrets detection with Trivy
- License compliance checking
- SARIF report generation for Security tab

### Documentation Workflow Features
- Markdown syntax validation
- Internal link checking
- Code example validation
- MkDocs site generation
- Automatic deployment to GitHub Pages
- Material theme with search functionality

### Performance Workflow Features
- Benchmark tests for core components
- Memory profiling and leak detection
- Response time monitoring
- Performance regression detection
- Artifact retention for comparison

### Release Workflow Features
- Automated changelog generation
- GitHub release creation
- PyPI package publishing
- Pre-release support (alpha, beta, rc)
- Asset uploading

---

*Last updated: This file will be automatically updated by the Workflow Status action*
*Status dashboard generated by: [status.yml](.github/workflows/status.yml)*
