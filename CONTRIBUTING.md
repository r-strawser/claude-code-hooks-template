# Contributing to Claude Code Hooks Template

First off, thank you for considering contributing to Claude Code Hooks Template! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone git@github.com:your-username/claude-code-hooks-template.git
   cd claude-code-hooks-template
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream git@github.com:r-strawser/claude-code-hooks-template.git
   ```

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- System information (OS, Python version, Claude Code version)
- Relevant logs from `logs/sessions/`
- Any error messages

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:

- A clear and descriptive title
- Detailed description of the proposed feature
- Use cases and benefits
- Possible implementation approach
- Any potential drawbacks or considerations

### Contributing Code

1. **Find an Issue**: Look for issues labeled `good first issue` or `help wanted`
2. **Comment**: Let others know you're working on it
3. **Branch**: Create a feature branch from `master`
4. **Code**: Make your changes following our coding standards
5. **Test**: Ensure your changes work correctly
6. **Document**: Update documentation as needed
7. **Submit**: Create a pull request

## Development Setup

### Prerequisites

- Python 3.8 or higher
- uv (Python package installer)
- Git
- Claude Code CLI

### Setting Up Your Development Environment

1. **Install dependencies**:
   ```bash
   # Install uv if not already installed
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Make hooks executable
   chmod +x .claude/hooks/*.py
   ```

2. **Create a test environment**:
   ```bash
   # Create logs directory
   mkdir -p logs/sessions
   
   # Test hooks
   echo '{}' | uv run .claude/hooks/pre_tool_use.py
   ```

3. **Set up pre-commit hooks** (optional):
   ```bash
   # Install pre-commit
   pip install pre-commit
   
   # Set up the git hook scripts
   pre-commit install
   ```

## Pull Request Process

1. **Update your fork**:
   ```bash
   git fetch upstream
   git checkout master
   git merge upstream/master
   ```

2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**:
   - Write clear, concise commit messages
   - Keep commits focused and atomic
   - Include tests if applicable

4. **Run tests**:
   ```bash
   # Test individual hooks
   python -m pytest tests/  # If tests exist
   
   # Manual testing
   echo '{"tool": "Bash", "params": {"command": "ls"}}' | uv run .claude/hooks/pre_tool_use.py
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**:
   - Use a clear title and description
   - Reference any related issues
   - Include screenshots/logs if relevant
   - Ensure all checks pass

## Coding Standards

### Python Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add type hints where appropriate
- Keep functions small and focused
- Document complex logic with comments

### Hook Development Guidelines

1. **Input/Output**:
   - Hooks receive JSON via stdin
   - Output should be minimal unless debugging
   - Use stderr for error messages
   - Exit with appropriate status codes

2. **Error Handling**:
   - Fail gracefully - don't crash Claude Code
   - Log errors appropriately
   - Provide helpful error messages

3. **Performance**:
   - Hooks should execute quickly (< 1 second)
   - Avoid blocking operations
   - Use caching where appropriate

4. **Security**:
   - Never log sensitive information
   - Validate all inputs
   - Be cautious with file system operations

### Example Hook Structure

```python
#!/usr/bin/env python3
"""Brief description of what this hook does."""

import json
import sys
from pathlib import Path
from typing import Dict, Any

def process_hook(data: Dict[str, Any]) -> None:
    """Process the hook data.
    
    Args:
        data: The JSON data from Claude Code
    """
    try:
        # Your hook logic here
        pass
    except Exception as e:
        print(f"Error in hook: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    try:
        data = json.load(sys.stdin)
        process_hook(data)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)
```

## Testing Guidelines

### Unit Tests

- Test individual functions and components
- Cover edge cases and error conditions
- Use meaningful test names
- Keep tests focused and independent

### Integration Tests

- Test hook integration with Claude Code
- Verify logging functionality
- Test safety features and blocks
- Ensure session management works correctly

### Manual Testing

Before submitting a PR, manually test:

1. All modified hooks work correctly
2. Safety features still block dangerous commands
3. Logging creates appropriate files
4. No regressions in existing functionality

## Documentation

### Code Documentation

- Add docstrings to all functions and classes
- Include parameter descriptions and return values
- Document any non-obvious logic
- Keep comments up-to-date with code changes

### README Updates

Update the README when:

- Adding new features
- Changing installation process
- Modifying configuration options
- Adding new hooks

### Changelog

For significant changes, update the changelog (if one exists) with:

- Version number
- Date
- List of changes (Added, Changed, Fixed, Removed)

## Questions?

If you have questions about contributing:

1. Check existing issues and discussions
2. Ask in the project's issue tracker
3. Reach out to maintainers

Thank you for contributing to Claude Code Hooks Template!