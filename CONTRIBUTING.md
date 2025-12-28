# Contributing to Reachy Email Notifier

Thank you for your interest in contributing to the Reachy Email Notifier project! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment (OS, Python version, Reachy model)
- Any error messages or logs

### Suggesting Enhancements

We welcome suggestions for new features! Please create an issue describing:
- The enhancement you'd like to see
- Why it would be useful
- How it might work

### Code Contributions

1. Fork the repository
2. Create a new branch for your feature (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Coding Standards

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions focused and single-purpose
- Comment complex logic

### Testing

Before submitting a PR:
- Test with demo mode (no robot required)
- If possible, test with actual Reachy hardware or simulation
- Ensure no errors with Gmail API integration
- Test edge cases (no internet, no emails, many emails, etc.)

## Ideas for Contributions

Here are some areas where contributions would be especially welcome:

### New Features
- Support for other email providers (Outlook, Yahoo, etc.)
- More animation varieties and customization
- Voice notifications using Reachy's audio capabilities
- Integration with other services (calendar, Slack, etc.)
- Configuration GUI or web interface
- Email filtering (only notify for important emails)
- Multiple user support

### Improvements
- Better error handling and recovery
- Performance optimizations
- More comprehensive documentation
- Example videos and tutorials
- Unit tests and integration tests
- CI/CD pipeline setup

### Bug Fixes
- Any bugs you encounter while using the app
- Edge cases not currently handled
- Platform-specific issues

## Development Setup

1. Clone your fork:
```bash
git clone https://github.com/yourusername/reachy-email-notifier.git
cd reachy-email-notifier
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install in development mode:
```bash
pip install -e .
```

4. Make your changes and test

## Community

- Be respectful and inclusive
- Help others in issues and discussions
- Share your Reachy email notifier setups and customizations
- Credit others for their contributions

## Questions?

If you have questions about contributing, feel free to:
- Open an issue with your question
- Reach out on the Pollen Robotics forum
- Check the existing issues and pull requests

Thank you for helping make Reachy Email Notifier better!
