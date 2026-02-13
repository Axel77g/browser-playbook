# Contributing to Scrapping Playbook Framework

Thank you for your interest in contributing to the Scrapping Playbook Framework! We're excited to have you join our community. This project aims to make web scraping accessible and maintainable through declarative YAML playbooks, and your contributions help make that vision a reality.

## How to Contribute

There are many ways you can contribute to this project:

### 🐛 Report Bugs

Found a bug? Please open an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Your environment (Python version, OS, browser engine)
- Sample playbook that demonstrates the issue (if applicable)

### 💡 Suggest Features

Have an idea for a new feature? We'd love to hear it! Please open an issue with:
- A clear description of the feature
- Use cases and benefits
- Possible implementation approach (optional)
- Example playbook syntax (if applicable)

### 📝 Improve Documentation

Documentation improvements are always welcome:
- Fix typos or unclear explanations
- Add more examples
- Improve API documentation
- Create tutorials or guides

### 🔧 Submit Pull Requests

Ready to write some code? Great! See the sections below for guidance.

### 🌐 Add New Browser Strategies

One of the most valuable contributions is adding support for new browser automation engines (Playwright, Puppeteer, etc.). See the "Adding a New Browser Strategy" section below.

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/scrapping-playbook-framework.git
cd scrapping-playbook-framework
```

### 2. Set Up Development Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt  # if requirements.txt exists

# Install development dependencies (if available)
pip install -r requirements-dev.txt  # if available
```

### 3. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 4. Make Your Changes

Write your code, add tests, and update documentation as needed.

### 5. Test Your Changes

```bash
# Run tests (if test suite exists)
python -m pytest

# Test your changes manually with example playbooks
python your_test_script.py
```

### 6. Commit Your Changes

```bash
git add .
git commit -m "Add a descriptive commit message"
```

Follow these commit message guidelines:
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests when relevant

### 7. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- A clear title and description
- Reference to any related issues
- Screenshots or examples (if applicable)

## Adding a New Browser Strategy

One of the most exciting ways to contribute is by adding support for a new browser automation engine. Here's how:

### Understanding the Strategy Pattern

The framework uses the Strategy Pattern to support multiple browser engines. Each engine implements the `WorkerStrategy` interface.

### Step-by-Step Guide

#### 1. Create Your Strategy Class

Create a new file in `worker_strategies/` directory (e.g., `playwright_worker_strategy.py`):

```python
from typing import Any
from scrapping_playbook_framework.worker_strategies.worker_strategy import WorkerStrategy
from scrapping_playbook_framework.task.task import ScrappingTask

class PlaywrightWorkerStrategy(WorkerStrategy):
    def get_available_tasks(self) -> dict[str, ScrappingTask[Any]]:
        """
        Returns a dictionary of available tasks for Playwright.
        Keys are task names (e.g., 'browser.goto', 'dom.get_element')
        Values are task instances.
        """
        from scrapping_playbook_framework.playwright.playwright_browser import PlaywrightBrowserTask
        from scrapping_playbook_framework.playwright.playwright_dom_task import PlaywrightDOMTask
        # Import other task implementations...
        
        return {
            "browser.goto": PlaywrightBrowserTask(),
            "dom.get_element": PlaywrightDOMTask(),
            "dom.get_elements": PlaywrightDOMTask(),
            # Add more tasks...
        }
```

#### 2. Implement Task Classes

Create engine-specific implementations for each task type in a new directory (e.g., `playwright/`):

**Example: Browser Task**

```python
from typing import Any
from scrapping_playbook_framework.task.browser_task import BrowserTask

class PlaywrightBrowserTask(BrowserTask):
    def execute(self, variables: dict[str, Any]) -> Any:
        """
        Implement browser navigation using Playwright.
        
        Args:
            variables: Dictionary containing 'url' and other parameters
            
        Returns:
            The page object or None
        """
        from playwright.sync_api import sync_playwright
        
        url = variables.get('url')
        if not url:
            raise ValueError("URL is required for browser.goto")
        
        # Implement Playwright-specific logic here
        # Return the page object or relevant result
        pass
```

**Example: DOM Task**

```python
from typing import Any
from scrapping_playbook_framework.task.dom_task import DOMTask

class PlaywrightDOMTask(DOMTask):
    def execute(self, variables: dict[str, Any]) -> Any:
        """
        Implement element queries using Playwright.
        """
        selector = variables.get('selector')
        # Implement Playwright selector logic
        pass
```

#### 3. Register Your Strategy

Add your strategy to the `strategies` dictionary in `worker.py`:

```python
from scrapping_playbook_framework.worker_strategies.playwright_worker_strategy import PlaywrightWorkerStrategy

class WorkerEngine(Enum):
    SELENIUM = "selenium"
    PLAYWRIGHT = "playwright"  # Add your engine
    PUPPETEER = "puppeteer"

strategies: dict[WorkerEngine, type[WorkerStrategy]] = {
    WorkerEngine.SELENIUM: SeleniumWorkerStrategy,
    WorkerEngine.PLAYWRIGHT: PlaywrightWorkerStrategy,  # Register here
}
```

#### 4. Implement Required Tasks

At minimum, implement these core tasks:
- **Browser navigation**: `browser.goto`
- **Element queries**: `dom.get_element`, `dom.get_elements`
- **Keyboard input**: `keyboard.type`, `keyboard.press`
- **Mouse actions**: `mouse.click`
- **Wait operations**: `wait`

#### 5. Handle Element Methods

Elements returned by `dom.get_element` should support these methods:
- `click()` - Click the element
- `get_text()` - Extract text content
- `get_attribute(attribute_name)` - Get attribute value
- `get_element(selector)` - Find child element

You'll need to create a wrapper class that implements these methods for your engine.

#### 6. Test Your Strategy

Create test playbooks and verify:
- All basic tasks work correctly
- Variables are properly stored and retrieved
- Loops and conditions function as expected
- Element methods work on returned elements

### Tips for Implementation

- **Look at Selenium implementation** - The `selenium/` directory contains reference implementations
- **Reuse base classes** - Extend the abstract task classes in `task/` directory
- **Handle errors gracefully** - Provide clear error messages
- **Document engine-specific quirks** - Note any limitations or special behaviors
- **Add type hints** - Use Python type hints for better IDE support
- **Keep it consistent** - Match the behavior of existing strategies

## Code Style

### Python Guidelines

- **Type Hints**: Use type hints for function parameters and return values
  ```python
  def execute(self, variables: dict[str, Any]) -> Any:
  ```

- **Docstrings**: Add docstrings to classes and public methods
  ```python
  def get_available_tasks(self) -> dict[str, ScrappingTask[Any]]:
      """
      Returns a dictionary mapping task names to task instances.
      
      Returns:
          Dictionary with task names as keys and ScrappingTask instances as values
      """
  ```

- **Naming Conventions**:
  - Classes: `PascalCase`
  - Functions/Methods: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`
  - Private attributes: `_leading_underscore`

- **Follow existing patterns**: Look at the codebase and match the existing style

### YAML Playbooks

- Use 2 spaces for indentation
- Use descriptive task names
- Add comments for complex operations
- Keep playbooks readable and maintainable

## Pull Request Process

1. **Update documentation** - If your change affects user-facing functionality, update the README.md
2. **Add examples** - For new features, add example playbooks to `examples/`
3. **Test thoroughly** - Ensure your changes work and don't break existing functionality
4. **Write clear descriptions** - Explain what your PR does and why
5. **Respond to feedback** - Be open to suggestions and iterate on your changes
6. **Keep PRs focused** - One feature or fix per PR is ideal

### PR Checklist

Before submitting, verify:
- [ ] Code follows the project's style guidelines
- [ ] Documentation is updated (if applicable)
- [ ] Examples are added (for new features)
- [ ] Changes have been tested
- [ ] Commit messages are clear and descriptive
- [ ] No unnecessary files are included (build artifacts, IDE config, etc.)

## Getting Help

- **Questions?** Open a discussion or issue on GitHub
- **Need clarification?** Comment on existing issues or PRs
- **Want to discuss a major change?** Open an issue first to discuss your approach

## Code of Conduct

This project follows a simple code of conduct:
- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Collaborate openly and honestly

## Recognition

All contributors will be recognized in the project. Your contributions, big or small, are valued and appreciated!

---

Thank you for contributing to Scrapping Playbook Framework! 🎉
