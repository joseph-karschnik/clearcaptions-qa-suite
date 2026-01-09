# ClearCaptions QA Suite - Setup Guide

## Prerequisites

### Required Software
- **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 16+** (for mobile testing) - [Download Node.js](https://nodejs.org/)
- **Chrome/Firefox** browsers
- **Git** - [Download Git](https://git-scm.com/downloads)

### Optional (for Mobile Testing)
- **Appium Server** - Install via npm: `npm install -g appium`
- **Android SDK** (for Android testing)
- **Xcode** (for iOS testing on Mac)

## Installation Steps

### 1. Clone or Navigate to Project
```bash
cd clearcaptions-qa-suite
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Node.js Dependencies (for mobile testing)
```bash
npm install
```

### 5. Set Up Appium (for mobile testing)
```bash
npm install -g appium
appium --version  # Verify installation
```

### 6. Configure Environment

#### Copy Configuration Files
```bash
# Copy example environment file
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# Edit .env and add your credentials
```

#### Update Configuration
1. Edit `config/config.yaml` with your environment URLs
2. Update `config/environments.yaml` with environment-specific settings
3. Add test credentials to `.env` file

### 7. Verify Installation
```bash
# Run a simple test to verify setup
pytest tests/web/test_home_page.py::TestHomePage::test_home_page_loads -v
```

## Configuration Details

### Environment Variables
Create a `.env` file with the following:
```
ADMIN_PASSWORD=your_password
TEST_USER_PASSWORD=your_password
API_KEY=your_api_key
TEST_ENV=staging
```

### Config Files
- `config/config.yaml` - Main configuration
- `config/environments.yaml` - Environment-specific settings

### Test Data
- `test_data/test_users.yaml` - Test user credentials
- `test_data/caption_test_cases.yaml` - Caption quality test cases

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test Suite
```bash
# Web tests
pytest tests/web/ -v

# Accessibility tests
pytest tests/accessibility/ -v

# Caption quality tests
pytest tests/caption_quality/ -v

# API tests
pytest tests/api/ -v

# Compliance tests
pytest tests/compliance/ -v
```

### Run by Marker
```bash
# Smoke tests
pytest -m smoke

# Regression tests
pytest -m regression

# Accessibility tests
pytest -m accessibility

# Compliance tests
pytest -m compliance
```

### Run with Specific Browser
```bash
pytest --browser=chrome
pytest --browser=firefox
```

### Generate Reports
```bash
# HTML report
pytest --html=reports/report.html --self-contained-html

# JSON report
pytest --json-report --json-report-file=reports/report.json

# With screenshots on failure
pytest --html=reports/report.html --self-contained-html
```

## CI/CD Integration

### GitHub Actions
Create `.github/workflows/qa-tests.yml`:
```yaml
name: QA Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: pytest --html=reports/report.html
      - uses: actions/upload-artifact@v2
        with:
          name: test-report
          path: reports/
```

### Jenkins
Add to Jenkinsfile:
```groovy
stage('QA Tests') {
    steps {
        sh 'pip install -r requirements.txt'
        sh 'pytest --html=reports/report.html'
        publishHTML([
            reportDir: 'reports',
            reportFiles: 'report.html',
            reportName: 'Test Report'
        ])
    }
}
```

## Troubleshooting

### Common Issues

1. **WebDriver not found**
   - Install ChromeDriver: `pip install webdriver-manager`
   - Or download manually and add to PATH

2. **Import errors**
   - Ensure virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`

3. **Configuration errors**
   - Verify `config/config.yaml` exists and is valid YAML
   - Check environment variables in `.env` file

4. **Accessibility tests fail**
   - Ensure axe-core is installed: `pip install axe-selenium-python`
   - Check browser compatibility

5. **Mobile tests fail**
   - Verify Appium server is running: `appium`
   - Check device/emulator is connected
   - Verify app paths in config

## Next Steps

1. Review test cases and customize for your needs
2. Add more test data as needed
3. Configure CI/CD pipeline
4. Set up test reporting dashboard
5. Add performance testing scenarios

## Support

For issues or questions, refer to:
- Framework documentation in `framework/` directory
- Test examples in `tests/` directory
- Configuration examples in `config/` directory
