"""
Login Page Object Model
"""
from selenium.webdriver.common.by import By
from framework.pages.base_page import BasePage
from loguru import logger


class LoginPage(BasePage):
    """Page Object for login page"""
    
    # Locators
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[type='email'], input[name*='email'], input[id*='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password'], input[name*='password'], input[id*='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit'], input[type='submit'], button:contains('Log in'), button:contains('Sign in')")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a[href*='forgot'], a:contains('Forgot')")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[role='alert'], .error, .alert-danger")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success, .alert-success")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/login"
    
    def load(self):
        """Load the login page"""
        self.navigate_to(self.url)
        logger.info("Login page loaded")
    
    def enter_email(self, email: str):
        """Enter email address"""
        self.send_keys(self.EMAIL_INPUT, email)
        logger.info(f"Entered email: {email}")
    
    def enter_password(self, password: str):
        """Enter password"""
        self.send_keys(self.PASSWORD_INPUT, password)
        logger.info("Entered password")
    
    def click_login(self):
        """Click login button"""
        self.click(self.LOGIN_BUTTON)
        logger.info("Clicked login button")
    
    def login(self, email: str, password: str):
        """Complete login flow"""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        logger.info("Login completed")
    
    def click_forgot_password(self):
        """Click forgot password link"""
        self.click(self.FORGOT_PASSWORD_LINK)
        logger.info("Clicked forgot password link")
    
    def get_error_message(self):
        """Get error message if present"""
        if self.is_displayed(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return None
    
    def is_error_displayed(self):
        """Check if error message is displayed"""
        return self.is_displayed(self.ERROR_MESSAGE)
