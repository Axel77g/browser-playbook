# Scrapping Playbook Framework

> A browser-agnostic web scraping framework inspired by Ansible

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.x](https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=flat&logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![YAML](https://img.shields.io/badge/YAML-Data%20Format-CB171E?style=flat&logo=yaml&logoColor=white)](https://yaml.org/)

## Introduction

Scrapping Playbook Framework is a powerful, declarative web scraping framework that lets you define your scraping tasks using simple YAML playbooks—just like Ansible. Say goodbye to writing repetitive boilerplate code for Selenium or Playwright. Instead, focus on **what** you want to scrape, not **how** to code it.

### Why Use This Framework?

- ✅ **Write Less Code**: Define scraping tasks in YAML instead of hundreds of lines of Python
- ✅ **Browser Agnostic**: Switch between Selenium, Playwright, and Puppeteer without changing your playbooks
- ✅ **Declarative**: Focus on what you want to achieve, not implementation details
- ✅ **Reusable**: Create playbook templates that work across different projects
- ✅ **Maintainable**: YAML playbooks are easier to read and modify than traditional scraping code

### Comparison

**Traditional Selenium Code:**
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
driver.get("https://example.com")
search_box = driver.find_element(By.CSS_SELECTOR, "input[name='q']")
search_box.click()
search_box.send_keys("web scraping")
# ... more boilerplate code
```

**With Scrapping Playbook Framework:**
```yaml
tasks:
  - name: Navigate to website
    action: browser.goto
    url: https://example.com
  
  - name: Find and click search box
    action: dom.get_element
    selector: "input[name='q']"
    output: search_box
  
  - name: Type search query
    action: keyboard.type
    text: "web scraping"
```

## Key Features

### 🎯 Browser Agnostic
Works seamlessly with multiple browser automation engines. Write your playbooks once, run them with any supported engine:
- **Selenium** (fully supported)
- **Playwright** (coming soon)
- **Puppeteer** (coming soon)

### 📝 YAML Playbooks
Define scraping tasks using intuitive YAML syntax, inspired by Ansible. No need to write repetitive browser automation code.

### 🔄 Loops & Conditions
Built-in support for iterations and conditional execution:
- Loop over lists of elements with `map`
- Execute tasks conditionally with `when` clauses
- Nested task execution for complex workflows

### 🧩 Modular Tasks
Reusable task system with pre-built actions for:
- Browser navigation
- DOM manipulation
- Keyboard and mouse interactions
- Element queries and data extraction
- Wait operations

### 🎭 Context Management
Powerful variable management system that maintains state across tasks:
- Store element references
- Pass data between tasks
- Use variables in conditions and loops

### ⚡ Strategy Pattern
Pluggable browser automation strategies make it easy to:
- Add support for new engines
- Switch engines without changing playbooks
- Extend functionality with custom tasks

## Installation

### From Source
```bash
git clone https://github.com/Axel77g/scrapping-playbook-framework.git
cd scrapping-playbook-framework
pip install -r requirements.txt  # if requirements.txt exists
```

### Prerequisites
- Python 3.x
- Selenium WebDriver (for Selenium engine)

## Quick Start

### 1. Create a Playbook

Create a file named `my_scraper.yaml`:

```yaml
tasks:
  - name: Navigate to website
    action: browser.goto
    url: https://example.com
    output: page

  - name: Find search box
    action: dom.get_element
    selector: "input[name='q']"
    output: search_box

  - name: Click search box
    action: $search_box.click

  - name: Type search query
    action: keyboard.type
    text: "web scraping"
```

### 2. Run the Playbook

```python
from scrapping_playbook_framework.worker import Worker, WorkerEngine
from scrapping_playbook_framework.playbook_reader import from_yaml_file

# Load playbook
playbook = from_yaml_file("my_scraper.yaml")

# Create worker with desired engine
worker = Worker(playbook, WorkerEngine.SELENIUM)

# Execute playbook
results = worker.start()

print(results)
```

## Architecture

The framework is built on a clean, modular architecture:

### Core Components

#### **Worker**
The main orchestrator that executes playbooks. It:
- Loads and validates playbooks
- Manages the execution context
- Coordinates task execution
- Handles loops and conditions

#### **PlaybookReader**
Parses YAML playbooks into structured task definitions using Pydantic models for validation.

#### **Tasks**
Individual actions that can be performed:
- **BrowserTask**: Navigation operations (`browser.goto`)
- **DOMTask**: Element queries (`dom.get_element`, `dom.get_elements`)
- **KeyboardTask**: Text input (`keyboard.type`, `keyboard.press`)
- **ClickTask**: Mouse operations (`mouse.click`)
- **WaitTask**: Delays and waits (`wait`)

#### **Strategies**
Browser-specific implementations of the task system:
- **SeleniumWorkerStrategy**: Selenium WebDriver implementation
- **PlaywrightWorkerStrategy**: Playwright implementation (planned)
- **PuppeteerWorkerStrategy**: Puppeteer implementation (planned)

Each strategy provides a `get_available_tasks()` method that returns the engine-specific task implementations.

#### **ExecutionContext**
Manages variables and state throughout playbook execution:
- Store and retrieve variables
- Pass data between tasks
- Maintain isolated contexts for loops
- Variable injection and cloning for sub-tasks

## Supported Engines

| Engine | Status | Description |
|--------|--------|-------------|
| ✅ Selenium | **Implemented** | Full support for Selenium WebDriver |
| 🚧 Playwright | Planned | Microsoft's modern browser automation tool |
| 🚧 Puppeteer | Planned | Google's headless Chrome automation library |

## Playbook Structure

### Task Attributes

Every task in a playbook can have these attributes:

| Attribute | Required | Description |
|-----------|----------|-------------|
| `name` | ✅ | Human-readable task name |
| `action` | ✅ | The action to perform (e.g., `browser.goto`, `dom.get_element`) |
| `output` | ❌ | Variable name to store the result |
| `when` | ❌ | List of conditions for conditional execution |
| `map` | ❌ | Variable name of list to iterate over |
| `tasks` | ❌ | Nested tasks for loops |
| `item_name` | ❌ | Variable name for each item in a loop (default: `item`) |

Additional attributes depend on the specific action being performed.

### Conditions

The `when` attribute accepts a list of conditions:

```yaml
- name: Close popup if exists
  action: $popup.click
  when:
    - variable: popup
      is_defined: true
```

Available condition operators:
- `is_defined: true/false` - Check if variable exists
- `equals: value` - Check equality
- `not_equals: value` - Check inequality
- `greater_than: number` - Numeric comparison
- `less_than: number` - Numeric comparison

### Loops

Use `map` to iterate over lists:

```yaml
- name: Process all products
  map: products
  item_name: product
  tasks:
    - name: Get product title
      action: $product.get_element
      selector: ".title"
      output: title
```

### Variable References

Reference variables using the `$` prefix:
- `$variable_name` - Use variable value
- `$element.method` - Call method on variable (e.g., `$element.click`)

## Available Actions

### Browser Actions

- `browser.goto` - Navigate to a URL
  ```yaml
  - name: Navigate to page
    action: browser.goto
    url: https://example.com
    output: page
  ```

### DOM Actions

- `dom.get_element` - Find a single element
  ```yaml
  - name: Find search box
    action: dom.get_element
    selector: "input[name='q']"
    output: search_box
  ```

- `dom.get_elements` - Find multiple elements
  ```yaml
  - name: Get all products
    action: dom.get_elements
    selector: ".product-card"
    output: products
  ```

### Keyboard Actions

- `keyboard.type` - Type text
  ```yaml
  - name: Type search query
    action: keyboard.type
    text: "web scraping"
  ```

- `keyboard.press` - Press a key
  ```yaml
  - name: Press Enter
    action: keyboard.press
    key: "Enter"
  ```

### Mouse Actions

- `mouse.click` - Click at coordinates
  ```yaml
  - name: Click at position
    action: mouse.click
    x: 100
    y: 200
  ```

### Wait Actions

- `wait` - Wait for a duration
  ```yaml
  - name: Wait for page load
    action: wait
    duration: 2
  ```

### Variable Methods

Call methods on stored element references:

- `$element.click` - Click an element
- `$element.get_text` - Extract text content
- `$element.get_attribute` - Get element attribute
  ```yaml
  - name: Get element attribute
    action: $element.get_attribute
    attribute_name: "href"
    output: link_url
  ```
- `$element.get_element` - Find child element
  ```yaml
  - name: Find child element
    action: $product.get_element
    selector: ".price"
    output: price
  ```

## Examples

Check out the `examples/` directory for complete playbook examples:

- **simple_navigation.yaml** - Basic browser navigation
- **form_filling.yaml** - Form interaction and submission
- **loop_scraping.yaml** - Extracting data from multiple elements
- **conditional_tasks.yaml** - Using conditions to handle dynamic content

See [examples/README.md](examples/README.md) for detailed explanations.

## Contributing

We welcome contributions! Whether you want to:
- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🔧 Add support for new browser engines

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Roadmap

### Upcoming Features

- [ ] **Playwright Support** - Add full Playwright engine implementation
- [ ] **Puppeteer Support** - Add full Puppeteer engine implementation
- [ ] **More Built-in Tasks** - Screenshot capture, file downloads, cookie management
- [ ] **Better Error Handling** - Detailed error messages and recovery strategies
- [ ] **Documentation Website** - Comprehensive docs with tutorials and API reference
- [ ] **Retry Mechanisms** - Automatic retry on failures
- [ ] **Parallel Execution** - Run multiple tasks concurrently
- [ ] **Plugin System** - Easy custom task registration
- [ ] **Visual Testing** - Screenshot comparison and visual regression testing

### Long-term Vision

- Package distribution via PyPI
- IDE extensions for playbook authoring
- Cloud-based execution platform
- Playbook marketplace

---

**Made with ❤️ by the open source community**
