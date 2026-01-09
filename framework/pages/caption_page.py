"""
Caption Interface Page Object Model
"""
from selenium.webdriver.common.by import By
from framework.pages.base_page import BasePage
from loguru import logger
import time


class CaptionPage(BasePage):
    """Page Object for caption interface"""
    
    # Locators
    CAPTION_DISPLAY = (By.CSS_SELECTOR, "[data-testid='caption-display'], .caption-text, #caption-display")
    CALL_BUTTON = (By.CSS_SELECTOR, "[data-testid='call-button'], button:contains('Call'), .call-button")
    END_CALL_BUTTON = (By.CSS_SELECTOR, "[data-testid='end-call'], button:contains('End'), .end-call")
    PHONE_NUMBER_INPUT = (By.CSS_SELECTOR, "input[type='tel'], input[name*='phone']")
    SETTINGS_BUTTON = (By.CSS_SELECTOR, "[data-testid='settings'], button:contains('Settings'), .settings-button")
    VOLUME_CONTROL = (By.CSS_SELECTOR, "[data-testid='volume'], input[type='range'][name*='volume']")
    CAPTION_SETTINGS = (By.CSS_SELECTOR, "[data-testid='caption-settings'], .caption-settings")
    LATENCY_INDICATOR = (By.CSS_SELECTOR, "[data-testid='latency'], .latency-indicator")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/caption"
    
    def load(self):
        """Load the caption page"""
        self.navigate_to(self.url)
        logger.info("Caption page loaded")
    
    def initiate_call(self, phone_number: str = None):
        """Initiate a call"""
        if phone_number:
            self.enter_phone_number(phone_number)
        self.click(self.CALL_BUTTON)
        logger.info("Call initiated")
        return time.time()  # Return timestamp for latency measurement
    
    def end_call(self):
        """End the call"""
        self.click(self.END_CALL_BUTTON)
        logger.info("Call ended")
    
    def enter_phone_number(self, phone_number: str):
        """Enter phone number"""
        self.send_keys(self.PHONE_NUMBER_INPUT, phone_number)
        logger.info(f"Entered phone number: {phone_number}")
    
    def get_caption_text(self, timeout=30):
        """Get current caption text"""
        try:
            element = self.wait_for_element(self.CAPTION_DISPLAY, timeout)
            return element.text
        except:
            logger.warning("Caption text not available")
            return ""
    
    def wait_for_caption(self, timeout=30):
        """Wait for caption to appear"""
        try:
            element = self.wait_for_element(self.CAPTION_DISPLAY, timeout)
            return element.text
        except:
            return None
    
    def get_latency(self):
        """Get latency indicator value if available"""
        if self.is_displayed(self.LATENCY_INDICATOR):
            return self.get_text(self.LATENCY_INDICATOR)
        return None
    
    def open_settings(self):
        """Open settings"""
        self.click(self.SETTINGS_BUTTON)
        logger.info("Settings opened")
    
    def adjust_volume(self, value: int):
        """Adjust volume (0-100)"""
        element = self.find_element(self.VOLUME_CONTROL)
        self.driver.execute_script(f"arguments[0].value = {value};", element)
        logger.info(f"Volume adjusted to {value}")
