"""
ADA compliance tests
Tests accessibility requirements for users with disabilities
"""
import pytest
from framework.base.base_test import BaseTest
from framework.pages.home_page import HomePage
from framework.utils.accessibility import AccessibilityTester
from framework.utils.config_loader import ConfigLoader
from loguru import logger


@pytest.mark.compliance
@pytest.mark.accessibility
class TestADACompliance(BaseTest):
    """Test cases for ADA compliance"""
    
    def setup_method(self):
        """Setup for each test"""
        super().setup_method()
        self.config = ConfigLoader().load_config()
        self.ada_requirements = self.config['compliance']['ada']
    
    def test_wcag_compliance_level(self):
        """Test WCAG compliance level requirement"""
        required_level = self.ada_requirements['wcag_compliance']
        
        home_page = HomePage(self.driver)
        home_page.load()
        
        accessibility_tester = AccessibilityTester(self.driver, wcag_level=required_level)
        results = accessibility_tester.comprehensive_accessibility_check()
        
        # Check compliance
        assert results['wcag_level'] == required_level, \
            f"WCAG level should be {required_level}"
        
        logger.info(f"WCAG {required_level} compliance check completed")
        logger.info(f"Total issues: {results['total_issues']}")
    
    def test_keyboard_navigation_requirement(self):
        """Test keyboard navigation requirement"""
        assert self.ada_requirements['keyboard_navigation'], \
            "ADA requires keyboard navigation support"
        
        home_page = HomePage(self.driver)
        home_page.load()
        
        accessibility_tester = AccessibilityTester(self.driver)
        
        # Test keyboard navigation on key elements
        if home_page.is_displayed(home_page.GET_STARTED_BUTTON):
            button = home_page.find_element(home_page.GET_STARTED_BUTTON)
            result = accessibility_tester.check_keyboard_navigation(button)
            
            assert result['focusable'], \
                f"Get Started button must be keyboard accessible. Issues: {result.get('issues', [])}"
            logger.info("Keyboard navigation requirement met")
    
    def test_screen_reader_support(self):
        """Test screen reader support requirement"""
        assert self.ada_requirements['screen_reader_support'], \
            "ADA requires screen reader support"
        
        home_page = HomePage(self.driver)
        home_page.load()
        
        accessibility_tester = AccessibilityTester(self.driver)
        results = accessibility_tester.check_aria_labels()
        
        # Check that interactive elements have accessible names
        issues = results.get('issues', [])
        total_elements = results.get('total_elements', 0)
        
        # Calculate percentage of elements with issues
        if total_elements > 0:
            issue_percentage = (len(issues) / total_elements) * 100
            assert issue_percentage < 20, \
                f"Too many elements lack screen reader support: {issue_percentage:.1f}%"
            logger.info(f"Screen reader support: {100 - issue_percentage:.1f}% of elements accessible")
    
    def test_comprehensive_ada_compliance(self):
        """Test comprehensive ADA compliance"""
        home_page = HomePage(self.driver)
        home_page.load()
        
        accessibility_tester = AccessibilityTester(self.driver)
        results = accessibility_tester.comprehensive_accessibility_check()
        
        # Check all ADA requirements
        assert results['wcag_level'] == self.ada_requirements['wcag_compliance'], \
            "WCAG compliance level must match ADA requirements"
        
        # Check that critical issues are minimal
        total_issues = results.get('total_issues', 0)
        assert total_issues < 100, \
            f"Too many accessibility issues for ADA compliance: {total_issues}"
        
        logger.info("Comprehensive ADA compliance check completed")
        logger.info(f"WCAG Level: {results['wcag_level']}")
        logger.info(f"Total Issues: {total_issues}")
