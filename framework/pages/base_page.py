"""
Base Page Object Model class
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger
from framework.utils.config_loader import ConfigLoader


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, driver):
        self.driver = driver
        self.config = ConfigLoader().load_config()
        self.wait = WebDriverWait(driver, self.config['browser']['implicit_wait'])
        self.base_url = self.config['app']['web']['base_url']
    
    def navigate_to(self, path: str = ""):
        """Navigate to page"""
        url = f"{self.base_url}{path}"
        logger.info(f"Navigating to: {url}")
        self.driver.get(url)
    
    def find_element(self, locator, timeout=None):
        """Find element with wait"""
        wait = WebDriverWait(self.driver, timeout or self.config['browser']['implicit_wait'])
        return wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator, timeout=None):
        """Find multiple elements with wait"""
        wait = WebDriverWait(self.driver, timeout or self.config['browser']['implicit_wait'])
        wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)
    
    def click(self, locator, timeout=None):
        """Click element"""
        element = self.find_element(locator, timeout)
        wait = WebDriverWait(self.driver, timeout or self.config['browser']['implicit_wait'])
        wait.until(EC.element_to_be_clickable(locator))
        element.click()
        logger.info(f"Clicked element: {locator}")
    
    def send_keys(self, locator, text, timeout=None):
        """Send keys to element"""
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
        logger.info(f"Sent keys to element: {locator}")
    
    def get_text(self, locator, timeout=None):
        """Get text from element"""
        element = self.find_element(locator, timeout)
        return element.text
    
    def is_displayed(self, locator, timeout=None):
        """Check if element is displayed"""
        try:
            element = self.find_element(locator, timeout)
            return element.is_displayed()
        except:
            return False
    
    def wait_for_element(self, locator, timeout=None):
        """Wait for element to be present"""
        wait = WebDriverWait(self.driver, timeout or self.config['browser']['implicit_wait'])
        return wait.until(EC.presence_of_element_located(locator))
    
    def get_title(self):
        """Get page title"""
        return self.driver.title
    
    def get_current_url(self):
        """Get current URL"""
        return self.driver.current_url
