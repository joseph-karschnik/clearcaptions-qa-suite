"""
Home Page Object Model
"""
from selenium.webdriver.common.by import By
from framework.pages.base_page import BasePage
from loguru import logger


class HomePage(BasePage):
    """Page Object for ClearCaptions home page"""
    
    # Locators
    LOGO = (By.CSS_SELECTOR, "[data-testid='logo'], .logo, header img")
    NAVIGATION_MENU = (By.CSS_SELECTOR, "nav, [role='navigation']")
    GET_STARTED_BUTTON = (By.CSS_SELECTOR, "[data-testid='get-started'], a[href*='get-started'], button:contains('Get Started')")
    LEARN_MORE_BUTTON = (By.CSS_SELECTOR, "[data-testid='learn-more'], a[href*='learn'], button:contains('Learn More')")
    PHONE_NUMBER_INPUT = (By.CSS_SELECTOR, "input[type='tel'], input[name*='phone']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
    FOOTER = (By.CSS_SELECTOR, "footer")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/"
    
    def load(self):
        """Load the home page"""
        self.navigate_to(self.url)
        logger.info("Home page loaded")
    
    def is_logo_displayed(self):
        """Check if logo is displayed"""
        return self.is_displayed(self.LOGO)
    
    def click_get_started(self):
        """Click Get Started button"""
        self.click(self.GET_STARTED_BUTTON)
        logger.info("Clicked Get Started button")
    
    def click_learn_more(self):
        """Click Learn More button"""
        self.click(self.LEARN_MORE_BUTTON)
        logger.info("Clicked Learn More button")
    
    def enter_phone_number(self, phone_number: str):
        """Enter phone number"""
        self.send_keys(self.PHONE_NUMBER_INPUT, phone_number)
        logger.info(f"Entered phone number: {phone_number}")
    
    def submit_form(self):
        """Submit form"""
        self.click(self.SUBMIT_BUTTON)
        logger.info("Form submitted")
    
    def is_navigation_visible(self):
        """Check if navigation menu is visible"""
        return self.is_displayed(self.NAVIGATION_MENU)
    
    def get_page_title(self):
        """Get page title"""
        return self.get_title()
