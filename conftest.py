"""
Pytest configuration and shared fixtures
"""
import pytest
import yaml
from pathlib import Path
from framework.utils.config_loader import ConfigLoader


@pytest.fixture(scope="session")
def config():
    """Load and return configuration"""
    return ConfigLoader().load_config()


@pytest.fixture(scope="session")
def test_data():
    """Load test data"""
    from test_data.test_data_loader import TestDataLoader
    loader = TestDataLoader()
    return {
        'users': loader.load_users(),
        'caption_cases': loader.load_caption_test_cases()
    }


@pytest.fixture
def test_user(test_data):
    """Get standard test user"""
    return test_data['users'].get('standard_user', {})


@pytest.fixture
def admin_user(test_data):
    """Get admin test user"""
    return test_data['users'].get('admin', {})


def pytest_configure(config):
    """Configure pytest markers"""
    config.addinivalue_line(
        "markers", "smoke: Smoke tests - critical path validation"
    )
    config.addinivalue_line(
        "markers", "regression: Regression test suite"
    )
    config.addinivalue_line(
        "markers", "accessibility: Accessibility compliance tests"
    )
    config.addinivalue_line(
        "markers", "caption_quality: Caption quality and accuracy tests"
    )
    config.addinivalue_line(
        "markers", "compliance: FCC and ADA compliance tests"
    )
    config.addinivalue_line(
        "markers", "api: API endpoint tests"
    )
    config.addinivalue_line(
        "markers", "web: Web application tests"
    )
    config.addinivalue_line(
        "markers", "mobile: Mobile application tests"
    )
    config.addinivalue_line(
        "markers", "performance: Performance and load tests"
    )
    config.addinivalue_line(
        "markers", "security: Security and privacy tests"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take longer to execute"
    )


def pytest_html_report_title(report):
    """Customize HTML report title"""
    report.title = "ClearCaptions QA Test Report"
