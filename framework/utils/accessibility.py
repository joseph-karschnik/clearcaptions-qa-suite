"""
Accessibility testing utilities
WCAG compliance, screen reader support, keyboard navigation
"""
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from axe_selenium_python import Axe
from loguru import logger
from typing import List, Dict, Any


class AccessibilityTester:
    """Accessibility testing utilities"""
    
    def __init__(self, driver, wcag_level: str = "AA"):
        self.driver = driver
        self.wcag_level = wcag_level
        self.axe = Axe(driver)
    
    def run_axe_audit(self) -> Dict[str, Any]:
        """Run axe accessibility audit"""
        try:
            self.axe.inject()
            results = self.axe.run()
            return {
                'violations': results.get('violations', []),
                'passes': results.get('passes', []),
                'incomplete': results.get('incomplete', []),
                'inapplicable': results.get('inapplicable', [])
            }
        except Exception as e:
            logger.error(f"Error running axe audit: {e}")
            return {'error': str(e)}
    
    def check_keyboard_navigation(self, element) -> Dict[str, Any]:
        """Test keyboard navigation for an element"""
        issues = []
        
        try:
            # Check if element is focusable
            if not element.is_displayed():
                issues.append("Element is not visible")
            
            # Try to focus element
            element.send_keys(Keys.TAB)
            
            # Check if element received focus
            focused = self.driver.switch_to.active_element == element
            if not focused:
                issues.append("Element cannot receive keyboard focus")
            
            return {
                'focusable': len(issues) == 0,
                'issues': issues
            }
        except Exception as e:
            logger.error(f"Error checking keyboard navigation: {e}")
            return {'focusable': False, 'issues': [str(e)]}
    
    def check_color_contrast(self, element, min_ratio: float = 4.5) -> Dict[str, Any]:
        """Check color contrast ratio (simplified - would need actual color values)"""
        # This is a placeholder - actual implementation would extract
        # foreground and background colors and calculate contrast ratio
        try:
            # Get computed styles
            bg_color = element.value_of_css_property('background-color')
            color = element.value_of_css_property('color')
            
            # Note: Actual contrast calculation would require color parsing
            # and luminance calculation per WCAG guidelines
            return {
                'checked': True,
                'foreground_color': color,
                'background_color': bg_color,
                'note': 'Full contrast calculation requires color parsing'
            }
        except Exception as e:
            logger.error(f"Error checking color contrast: {e}")
            return {'checked': False, 'error': str(e)}
    
    def check_aria_labels(self) -> Dict[str, Any]:
        """Check for proper ARIA labels"""
        issues = []
        
        try:
            # Find interactive elements without labels
            interactive_elements = self.driver.find_elements(
                "css selector",
                "button, a, input, select, textarea, [role='button'], [role='link']"
            )
            
            for element in interactive_elements:
                aria_label = element.get_attribute('aria-label')
                aria_labelledby = element.get_attribute('aria-labelledby')
                text = element.text
                title = element.get_attribute('title')
                
                if not any([aria_label, aria_labelledby, text, title]):
                    issues.append({
                        'element': element.tag_name,
                        'issue': 'Missing accessible name'
                    })
            
            return {
                'checked': True,
                'issues': issues,
                'total_elements': len(interactive_elements)
            }
        except Exception as e:
            logger.error(f"Error checking ARIA labels: {e}")
            return {'checked': False, 'error': str(e)}
    
    def check_heading_structure(self) -> Dict[str, Any]:
        """Check for proper heading hierarchy"""
        issues = []
        
        try:
            headings = self.driver.find_elements("css selector", "h1, h2, h3, h4, h5, h6")
            heading_levels = [int(h.tag_name[1]) for h in headings]
            
            # Check for skipped levels
            for i in range(1, len(heading_levels)):
                if heading_levels[i] > heading_levels[i-1] + 1:
                    issues.append({
                        'position': i,
                        'issue': f'Heading level skipped from h{heading_levels[i-1]} to h{heading_levels[i]}'
                    })
            
            # Check for multiple h1 tags (should typically be one)
            h1_count = sum(1 for level in heading_levels if level == 1)
            if h1_count > 1:
                issues.append({
                    'issue': f'Multiple h1 tags found: {h1_count}'
                })
            
            return {
                'checked': True,
                'total_headings': len(headings),
                'h1_count': h1_count,
                'issues': issues
            }
        except Exception as e:
            logger.error(f"Error checking heading structure: {e}")
            return {'checked': False, 'error': str(e)}
    
    def comprehensive_accessibility_check(self) -> Dict[str, Any]:
        """Run comprehensive accessibility checks"""
        results = {
            'axe_audit': self.run_axe_audit(),
            'aria_labels': self.check_aria_labels(),
            'heading_structure': self.check_heading_structure(),
            'wcag_level': self.wcag_level
        }
        
        # Determine overall compliance
        axe_violations = len(results['axe_audit'].get('violations', []))
        aria_issues = len(results['aria_labels'].get('issues', []))
        heading_issues = len(results['heading_structure'].get('issues', []))
        
        total_issues = axe_violations + aria_issues + heading_issues
        results['compliant'] = total_issues == 0
        results['total_issues'] = total_issues
        
        return results
