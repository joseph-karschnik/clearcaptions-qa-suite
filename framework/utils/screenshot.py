"""
Screenshot helper utility
"""
import os
from datetime import datetime
from pathlib import Path
from loguru import logger


class ScreenshotHelper:
    """Helper class for taking and managing screenshots"""
    
    def __init__(self, driver, output_dir: str = "reports/screenshots"):
        self.driver = driver
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def capture(self, name: str = None) -> str:
        """Capture a screenshot"""
        if not name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"screenshot_{timestamp}"
        
        # Sanitize filename
        filename = name.replace(" ", "_").replace("::", "_")
        filepath = self.output_dir / f"{filename}.png"
        
        try:
            self.driver.save_screenshot(str(filepath))
            logger.info(f"Screenshot saved: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
            return None
    
    def capture_element(self, element, name: str = None) -> str:
        """Capture screenshot of a specific element"""
        if not name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"element_{timestamp}"
        
        filename = name.replace(" ", "_").replace("::", "_")
        filepath = self.output_dir / f"{filename}.png"
        
        try:
            element.screenshot(str(filepath))
            logger.info(f"Element screenshot saved: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Failed to capture element screenshot: {e}")
            return None
