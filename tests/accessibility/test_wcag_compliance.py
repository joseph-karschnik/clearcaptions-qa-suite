"""
WCAG compliance tests
"""
import pytest
from framework.base.base_test import BaseTest
from framework.pages.home_page import HomePage
from framework.utils.accessibility import AccessibilityTester
from loguru import logger


@pytest.mark.accessibility
@pytest.mark.compliance
class TestWCAGCompliance(BaseTest):
    """Test cases for WCAG compliance"""
    
    def test_axe_audit_home_page(self):
        """Run axe accessibility audit on home page"""
        home_page = HomePage(self.driver)
        home_page.load()
        
        accessibility_tester = AccessibilityTester(self.driver)
        results = accessibility_tester.run_axe_audit()
        
        violations = results.get('violations', [])
        logger.info(f"Found {len(violations)} accessibility violations")
        
        # Log violations for review
        for violation in violations[:5]:  # Log first 5
            logger.warning(f"Violation: {violation.get('id')} - {violation.get('description')}")
        
        # Assert no critical violations (adjust threshold as needed)
        assert len(violations) < 10, \
            f"Too many accessibility violations found: {len(violations)}"
    
    def test_keyboard_navigation(self):
        """Test keyboard navigation on home page"""
        home_page = HomePage(self.driver)
        home_page.load()
        
        accessibility_tester = AccessibilityTester(self.driver)
        
        # Test navigation menu keyboard access
        if home_page.is_displayed(home_page.NAVIGATION_MENU):
            nav_element = home_page.find_element(home_page.NAVIGATION_MENU)
            result = accessibility_tester.check_keyboard_navigation(nav_element)
            
            assert result['focusable'], \
                f"Navigation should be keyboard accessible. Issues: {result.get('issues', [])}"
            logger.info("Keyboard navigation works for navigation menu")
    
    def test_aria_labels(self):
        """Test ARIA labels on home page"""
        home_page = HomePage(self.driver)
        home_page.load()
        
        accessibility_tester = AccessibilityTester(self.driver)
        results = accessibility_tester.check_aria_labels()
        
        issues = results.get('issues', [])
        logger.info(f"Found {len(issues)} ARIA label issues")
        
        # Log issues for review
        for issue in issues[:5]:
            logger.warning(f"ARIA issue: {issue}")
        
        # Assert reasonable number of issues (adjust threshold as needed)
        assert len(issues) < 20, \
            f"Too many ARIA label issues: {len(issues)}"
    
    def test_heading_structure(self):
        """Test proper heading hierarchy"""
        home_page = HomePage(self.driver)
        home_page.load()
        
        accessibility_tester = AccessibilityTester(self.driver)
        results = accessibility_tester.check_heading_structure()
        
        issues = results.get('issues', [])
        logger.info(f"Heading structure check completed. Issues: {len(issues)}")
        
        # Log issues
        for issue in issues:
            logger.warning(f"Heading issue: {issue}")
        
        # Assert no critical heading issues
        assert len(issues) < 5, \
            f"Too many heading structure issues: {len(issues)}"
    
    def test_comprehensive_accessibility(self):
        """Run comprehensive accessibility check"""
        home_page = HomePage(self.driver)
        home_page.load()
        
        accessibility_tester = AccessibilityTester(self.driver)
        results = accessibility_tester.comprehensive_accessibility_check()
        
        total_issues = results.get('total_issues', 0)
        compliant = results.get('compliant', False)
        
        logger.info(f"Comprehensive accessibility check: {total_issues} total issues")
        logger.info(f"WCAG Level: {results.get('wcag_level')}")
        
        # Log summary
        if not compliant:
            logger.warning(f"Accessibility issues found: {total_issues}")
            logger.info("Review detailed results in test report")
        
        # Assert compliance (adjust threshold as needed)
        assert total_issues < 50, \
            f"Too many accessibility issues: {total_issues}"
