# Example Playbooks

This directory contains example playbooks demonstrating various features of the Scrapping Playbook Framework.

## Running the Examples

To run any of these examples, use the following Python code:

```python
from scrapping_playbook_framework.worker import Worker, WorkerEngine
from scrapping_playbook_framework.playbook_reader import from_yaml_file

# Load the playbook
playbook = from_yaml_file("examples/simple_navigation.yaml")

# Create a worker with Selenium engine
worker = Worker(playbook, WorkerEngine.SELENIUM)

# Execute the playbook
results = worker.start()

print(results)
```

## Examples Overview

### 1. simple_navigation.yaml

**Purpose**: Demonstrates basic browser navigation and waiting.

**What it does**:
- Navigates to GitHub's homepage
- Waits for 2 seconds to ensure the page loads

**Key concepts**:
- `browser.goto` action for navigation
- `wait` action for delays
- Using `output` to store page reference

**Use this when**: You need to load a webpage and wait for it to render.

```bash
python run_example.py examples/simple_navigation.yaml
```

---

### 2. form_filling.yaml

**Purpose**: Shows how to interact with form elements.

**What it does**:
- Navigates to a login page
- Finds username and password input fields
- Fills in the form fields
- Clicks the submit button

**Key concepts**:
- `dom.get_element` to find elements by CSS selector
- Variable storage with `output`
- Variable method calls like `$username_field.click`
- `keyboard.type` for text input
- Chaining tasks to complete a workflow

**Use this when**: You need to fill out forms, login pages, or interact with input fields.

**Note**: Replace `https://example.com/login` with an actual login URL to test this playbook.

---

### 3. loop_scraping.yaml

**Purpose**: Demonstrates looping over multiple elements to process data.

**What it does**:
- Navigates to a product listing page
- Finds all product cards on the page
- Loops through each product to extract:
  - Product title
  - Product price

**Key concepts**:
- `dom.get_elements` to find multiple elements
- `map` attribute to loop over a list
- `item_name` to name the loop variable
- Nested `tasks` within a loop
- Extracting child elements with `$product.get_element`
- Getting text content with `$element.get_text`

**Use this when**: You need to process data from multiple similar elements (product lists, article lists, table rows, etc.).

**Common patterns**:
- E-commerce product information gathering
- News article extraction
- Social media post collection
- Search result processing

---

### 4. conditional_tasks.yaml

**Purpose**: Shows how to use conditional execution based on element existence.

**What it does**:
- Navigates to a webpage
- Checks if a popup modal exists
- Closes the popup only if it's present
- Continues with the main task

**Key concepts**:
- `when` attribute for conditional execution
- `is_defined` condition to check variable existence
- Handling optional elements gracefully
- Preventing errors from missing elements

**Use this when**: 
- Dealing with dynamic content that may or may not appear
- Handling popups, modals, or dismissible notifications
- Working with A/B tested pages
- Managing optional page elements

**Real-world scenarios**:
- Cookie consent banners
- Newsletter subscription popups
- Age verification modals
- Regional content variations

---

## Advanced Usage Tips

### Combining Multiple Patterns

You can combine loops, conditions, and nested tasks for complex automation scenarios:

```yaml
tasks:
  - name: Get all articles
    action: dom.get_elements
    selector: ".article"
    output: articles
  
  - name: Process articles
    map: articles
    item_name: article
    tasks:
      - name: Check if article has image
        action: $article.get_element
        selector: "img"
        output: article_image
      
      - name: Extract image URL only if exists
        action: $article_image.get_attribute
        attribute_name: "src"
        output: image_url
        when:
          - variable: article_image
            is_defined: true
```

### Error Handling

Always use conditions when dealing with optional elements to prevent playbook failures:

```yaml
- name: Find optional banner
  action: dom.get_element
  selector: ".banner"
  output: banner

- name: Close banner if present
  action: $banner.click
  when:
    - variable: banner
      is_defined: true
```

### Performance Optimization

- Use appropriate wait durations (don't wait longer than necessary)
- Query for multiple elements at once when possible
- Minimize navigation actions (they're typically slow)

### Debugging Tips

1. **Start small**: Test individual tasks before combining them
2. **Use descriptive names**: Clear task names help identify where issues occur
3. **Check outputs**: Store intermediate results in variables to inspect them
4. **Add wait steps**: If elements aren't found, try adding small waits

## Creating Your Own Playbooks

When creating new playbooks:

1. **Plan your workflow**: Write down the steps you'd take manually
2. **Identify selectors**: Use browser dev tools to find CSS selectors
3. **Test selectors**: Verify selectors work in the browser console
4. **Build incrementally**: Add tasks one at a time and test
5. **Handle edge cases**: Use conditions for optional elements
6. **Add comments**: Document complex logic in your YAML

## Need Help?

- Check the main [README.md](../README.md) for action reference
- Review [CONTRIBUTING.md](../CONTRIBUTING.md) for development setup
- Open an issue on GitHub for questions or bugs

---

Happy automating! 🎯
