"""
Base test class providing common functionality for all tests
"""
import pytest
import yaml
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from loguru import logger
from framework.utils.config_loader import ConfigLoader
from framework.utils.screenshot import ScreenshotHelper


class BaseTest:
    """Base test class with common setup and teardown"""
    
    def __init__(self):
        self.driver = None
        self.config = ConfigLoader().load_config()
        self.screenshot_helper = None
        self.wait = None
    
    @pytest.fixture(autouse=True)
    def setup(self, request):
        """Setup fixture that runs before each test"""
        # Initialize driver
        self.driver = self._init_driver()
        self.wait = WebDriverWait(self.driver, self.config['browser']['implicit_wait'])
        self.screenshot_helper = ScreenshotHelper(self.driver)
        
        # Set test name for reporting
        self.test_name = request.node.name
        
        yield
        
        # Teardown
        self._teardown()
    
    def _init_driver(self):
        """Initialize WebDriver based on configuration"""
        browser = self.config['browser']['default']
        headless = self.config['browser']['headless']
        
        if browser.lower() == 'chrome':
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument('--headless')
            for opt in self.config['browser']['options']:
                options.add_argument(opt)
            driver = webdriver.Chrome(options=options)
        elif browser.lower() == 'firefox':
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument('--headless')
            driver = webdriver.Firefox(options=options)
        else:
            raise ValueError(f"Unsupported browser: {browser}")
        
        # Set window size
        width, height = self.config['browser']['window_size'].split('x')
        driver.set_window_size(int(width), int(height))
        
        return driver
    
    def _teardown(self):
        """Cleanup after test execution"""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                logger.error(f"Error closing driver: {e}")
    
    def navigate_to(self, url):
        """Navigate to a URL"""
        full_url = f"{self.config['app']['web']['base_url']}{url}"
        logger.info(f"Navigating to: {full_url}")
        self.driver.get(full_url)
    
    def wait_for_element(self, locator, timeout=None):
        """Wait for element to be present"""
        timeout = timeout or self.config['browser']['implicit_wait']
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))
    
    def wait_for_clickable(self, locator, timeout=None):
        """Wait for element to be clickable"""
        timeout = timeout or self.config['browser']['implicit_wait']
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def take_screenshot(self, name=None):
        """Take a screenshot"""
        if not name:
            name = self.test_name
        return self.screenshot_helper.capture(name)
    
    def get_page_title(self):
        """Get current page title"""
        return self.driver.title
    
    def get_current_url(self):
        """Get current URL"""
        return self.driver.current_url
