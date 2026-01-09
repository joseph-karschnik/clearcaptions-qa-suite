# Contributing to ClearCaptions QA Suite

## Code Standards

### Python Style Guide
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for all classes and functions
- Keep functions focused and single-purpose

### Test Structure
- Use descriptive test names: `test_<feature>_<expected_behavior>`
- One assertion per test when possible
- Use fixtures for setup/teardown
- Group related tests in classes

### Page Object Model
- One page object per page/screen
- Locators defined as class attributes
- Methods represent user actions
- No assertions in page objects

## Adding New Tests

### 1. Web Tests
```python
# tests/web/test_new_feature.py
import pytest
from framework.base.base_test import BaseTest
from framework.pages.new_page import NewPage

@pytest.mark.web
class TestNewFeature(BaseTest):
    def test_feature_works(self):
        page = NewPage(self.driver)
        page.load()
        # Test implementation
```

### 2. Accessibility Tests
```python
# tests/accessibility/test_new_accessibility.py
import pytest
from framework.base.base_test import BaseTest
from framework.utils.accessibility import AccessibilityTester

@pytest.mark.accessibility
class TestNewAccessibility(BaseTest):
    def test_accessibility_feature(self):
        # Test implementation
```

### 3. Caption Quality Tests
```python
# tests/caption_quality/test_new_quality.py
import pytest
from framework.utils.caption_quality import CaptionQualityAnalyzer

@pytest.mark.caption_quality
class TestNewQuality:
    def test_quality_metric(self):
        analyzer = CaptionQualityAnalyzer()
        # Test implementation
```

## Adding New Page Objects

```python
# framework/pages/new_page.py
from selenium.webdriver.common.by import By
from framework.pages.base_page import BasePage

class NewPage(BasePage):
    # Locators
    ELEMENT = (By.CSS_SELECTOR, "selector")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/new-page"
    
    def load(self):
        self.navigate_to(self.url)
    
    def action_method(self):
        self.click(self.ELEMENT)
```

## Adding New Utilities

```python
# framework/utils/new_utility.py
from loguru import logger

class NewUtility:
    def __init__(self):
        pass
    
    def utility_method(self):
        logger.info("Utility method executed")
        return result
```

## Test Data Management

- Add test data to `test_data/` directory
- Use YAML format for structured data
- Keep sensitive data in `.env` file
- Document test data structure

## Reporting

- Use appropriate log levels (info, warning, error)
- Include context in log messages
- Take screenshots on failures
- Generate comprehensive reports

## Pull Request Process

1. Create feature branch
2. Write tests for new functionality
3. Ensure all tests pass
4. Update documentation
5. Submit pull request with description

## Questions?

Refer to existing test files for examples and patterns.
