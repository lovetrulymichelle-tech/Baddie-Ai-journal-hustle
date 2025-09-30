# Contributing to Baddie AI Journal Hustle

Thank you for your interest in contributing to Baddie AI Journal Hustle! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## Getting Started

Before you begin:
- Make sure you have Python 3.8+ installed
- Familiarize yourself with the project by reading the [README.md](README.md)
- Check the [.github/copilot-instructions.md](.github/copilot-instructions.md) for detailed project architecture and guidelines

## Development Setup

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/Baddie-Ai-journal-hustle.git
   cd Baddie-Ai-journal-hustle
   ```

2. **Create a Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # venv\Scripts\activate   # On Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation**
   ```bash
   python check_deployment.py
   ```
   All checks should pass before proceeding.

5. **Run Tests**
   ```bash
   python test_swarms.py
   python test_subscription.py
   ```

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **Bug Fixes**: Found a bug? Submit a fix!
- **Feature Development**: New features that enhance the application
- **Documentation**: Improvements to docs, comments, or examples
- **Testing**: Additional test cases or test infrastructure improvements
- **Performance**: Optimizations and performance improvements

### Before Starting Work

1. **Check Existing Issues**: Look for existing issues or create a new one
2. **Discuss Major Changes**: For significant changes, open an issue first to discuss
3. **Claim an Issue**: Comment on the issue to let others know you're working on it
4. **Create a Branch**: Use a descriptive branch name (e.g., `feature/add-export`, `fix/streak-calculation`)

## Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions, classes, and modules
- Keep functions focused and concise

### Code Quality Tools

We use the following tools (check .flake8 for configuration):
```bash
# Check code style
flake8 .

# Format code (if black is installed)
black .
```

### Documentation

- Update docstrings when modifying functions
- Update README.md if adding new features
- Update .github/copilot-instructions.md for architecture changes
- Add inline comments for complex logic

## Testing Guidelines

### Running Tests

```bash
# Core functionality tests
python test_swarms.py

# Subscription system tests
python test_subscription.py

# Deployment verification
python check_deployment.py

# Full application demo
python demo.py
```

### Writing Tests

- Test files use direct Python execution (not pytest)
- Include both success and error cases
- Use descriptive test names and output messages
- Tests should be self-contained and not depend on external state

### Test Coverage

- Add tests for new features
- Ensure bug fixes include regression tests
- Test both happy path and edge cases

## Pull Request Process

### Before Submitting

1. **Update Your Branch**
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Run All Tests**
   ```bash
   python check_deployment.py
   python test_swarms.py
   python test_subscription.py
   ```

3. **Check Code Style**
   ```bash
   flake8 .
   ```

4. **Update Documentation**
   - Update README.md if needed
   - Update docstrings
   - Add comments for complex changes

### PR Submission Checklist

- [ ] Tests pass locally
- [ ] Code follows project style guidelines
- [ ] Documentation is updated
- [ ] Commit messages are clear and descriptive
- [ ] Branch is up-to-date with main
- [ ] PR description clearly explains the changes
- [ ] Related issue is referenced (if applicable)

### PR Title Format

Use clear, descriptive titles:
- `feat: Add CSV export for journal entries`
- `fix: Correct streak calculation for DST transitions`
- `docs: Update deployment instructions for Railway`
- `test: Add tests for mood analysis edge cases`

### PR Description Template

```markdown
## Description
Brief description of changes

## Related Issue
Fixes #123

## Changes Made
- List of changes
- Another change

## Testing Done
- How you tested the changes
- Test results

## Screenshots (if applicable)
Add screenshots for UI changes
```

## Issue Reporting

### Before Creating an Issue

1. Search existing issues to avoid duplicates
2. Check if the issue is already fixed in the latest version
3. Gather relevant information (error messages, steps to reproduce)

### Issue Template

Use the appropriate issue template:
- **Bug Report**: For reporting bugs
- **Feature Request**: For suggesting new features
- **Documentation**: For documentation improvements
- **Question**: For asking questions about the project

### Include in Bug Reports

- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages or logs
- Relevant configuration (environment variables, etc.)

## Development Workflow

### Typical Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make Changes**
   - Write code following coding standards
   - Add/update tests
   - Update documentation

3. **Test Locally**
   ```bash
   python test_swarms.py
   python test_subscription.py
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: descriptive commit message"
   ```

5. **Push to Your Fork**
   ```bash
   git push origin feature/my-feature
   ```

6. **Create Pull Request**
   - Go to GitHub and create a PR
   - Fill out the PR template
   - Link related issues

### Commit Message Guidelines

Use conventional commit format:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions or modifications
- `refactor:` Code refactoring
- `style:` Code style changes (formatting, etc.)
- `chore:` Maintenance tasks

## Environment Variables

For local development, copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Required for development:
- `SECRET_KEY`: Flask secret key
- `SQLALCHEMY_DATABASE_URI`: Database connection (optional, defaults to SQLite)

Optional:
- `OPENAI_API_KEY`: For AI features
- `STRIPE_SECRET_KEY`: For subscription features

## Database Changes

If you modify database models:

1. Test with SQLite first (local development)
2. Test with PostgreSQL (production environment)
3. Update migration scripts if needed
4. Document schema changes in PR description

## Getting Help

- **Questions**: Open an issue with the "Question" label
- **Discussions**: Use GitHub Discussions for general questions
- **Documentation**: Check .github/copilot-instructions.md for detailed info
- **GitHub Copilot**: The repository is configured for Copilot assistance

## Recognition

Contributors will be recognized in:
- GitHub contributor list
- Release notes for significant contributions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to Baddie AI Journal Hustle! 🎉
