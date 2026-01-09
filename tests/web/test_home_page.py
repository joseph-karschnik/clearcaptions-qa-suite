"""
Web tests for home page
"""
import pytest
from framework.base.base_test import BaseTest
from framework.pages.home_page import HomePage
from loguru import logger


@pytest.mark.web
@pytest.mark.smoke
class TestHomePage(BaseTest):
    """Test cases for home page"""
    
    def test_home_page_loads(self):
        """Test that home page loads successfully"""
        home_page = HomePage(self.driver)
        home_page.load()
        
        assert home_page.get_page_title(), "Page title should be present"
        logger.info("Home page loaded successfully")
    
    def test_logo_displayed(self):
        """Test that logo is displayed"""
        home_page = HomePage(self.driver)
        home_page.load()
        
        assert home_page.is_logo_displayed(), "Logo should be displayed"
        logger.info("Logo is displayed")
    
    def test_navigation_menu_visible(self):
        """Test that navigation menu is visible"""
        home_page = HomePage(self.driver)
        home_page.load()
        
        assert home_page.is_navigation_visible(), "Navigation menu should be visible"
        logger.info("Navigation menu is visible")
    
    @pytest.mark.regression
    def test_get_started_button(self):
        """Test Get Started button functionality"""
        home_page = HomePage(self.driver)
        home_page.load()
        
        # Check if button exists and is clickable
        assert home_page.is_displayed(home_page.GET_STARTED_BUTTON), \
            "Get Started button should be displayed"
        logger.info("Get Started button is present")
    
    def test_phone_number_input(self):
        """Test phone number input field"""
        home_page = HomePage(self.driver)
        home_page.load()
        
        test_phone = "+15551234567"
        home_page.enter_phone_number(test_phone)
        
        # Verify phone number was entered
        element = home_page.find_element(home_page.PHONE_NUMBER_INPUT)
        assert element.get_attribute('value') == test_phone, \
            "Phone number should be entered correctly"
        logger.info("Phone number input works correctly")
