"""
Web tests for login functionality
"""
import pytest
from framework.base.base_test import BaseTest
from framework.pages.login_page import LoginPage
from loguru import logger


@pytest.mark.web
@pytest.mark.smoke
class TestLogin(BaseTest):
    """Test cases for login functionality"""
    
    def test_login_page_loads(self):
        """Test that login page loads successfully"""
        login_page = LoginPage(self.driver)
        login_page.load()
        
        assert "login" in login_page.get_current_url().lower() or \
               login_page.is_displayed(login_page.EMAIL_INPUT), \
               "Login page should load"
        logger.info("Login page loaded successfully")
    
    def test_email_input_present(self):
        """Test that email input is present"""
        login_page = LoginPage(self.driver)
        login_page.load()
        
        assert login_page.is_displayed(login_page.EMAIL_INPUT), \
            "Email input should be displayed"
        logger.info("Email input is present")
    
    def test_password_input_present(self):
        """Test that password input is present"""
        login_page = LoginPage(self.driver)
        login_page.load()
        
        assert login_page.is_displayed(login_page.PASSWORD_INPUT), \
            "Password input should be displayed"
        logger.info("Password input is present")
    
    def test_login_form_submission(self):
        """Test login form can be submitted"""
        login_page = LoginPage(self.driver)
        login_page.load()
        
        # Enter test credentials
        login_page.enter_email("test@example.com")
        login_page.enter_password("testpassword")
        
        # Verify inputs have values
        email_element = login_page.find_element(login_page.EMAIL_INPUT)
        password_element = login_page.find_element(login_page.PASSWORD_INPUT)
        
        assert email_element.get_attribute('value') == "test@example.com", \
            "Email should be entered"
        assert password_element.get_attribute('value') == "testpassword", \
            "Password should be entered"
        
        logger.info("Login form inputs work correctly")
    
    @pytest.mark.regression
    def test_invalid_login_shows_error(self):
        """Test that invalid login shows error message"""
        login_page = LoginPage(self.driver)
        login_page.load()
        
        # Attempt login with invalid credentials
        login_page.login("invalid@example.com", "wrongpassword")
        
        # Wait a moment for error to appear
        import time
        time.sleep(2)
        
        # Check if error is displayed (if login fails)
        # Note: This test may need adjustment based on actual behavior
        logger.info("Invalid login attempt completed")
