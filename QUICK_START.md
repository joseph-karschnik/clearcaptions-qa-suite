# Quick Start Guide - ClearCaptions QA Suite

## 5-Minute Setup

### Step 1: Install Dependencies
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install packages
pip install -r requirements.txt
```

### Step 2: Configure
```bash
# Copy environment file
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux

# Edit .env and add your credentials
```

### Step 3: Run Your First Test
```bash
# Run a simple web test
pytest tests/web/test_home_page.py::TestHomePage::test_home_page_loads -v
```

## Common Commands

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
```

### Run by Category
```bash
# Smoke tests only
pytest -m smoke

# All compliance tests
pytest -m compliance
```

### Generate Report
```bash
pytest --html=reports/report.html --self-contained-html
```

## Test Structure

```
tests/
├── web/              # Web application tests
├── mobile/           # Mobile app tests
├── api/              # API endpoint tests
├── accessibility/    # WCAG/ADA compliance
├── caption_quality/  # Caption accuracy tests
└── compliance/       # FCC/ADA regulatory tests
```

## Key Features

✅ **Web Testing** - Selenium-based web UI testing  
✅ **Mobile Testing** - Appium-based mobile app testing  
✅ **API Testing** - REST API endpoint validation  
✅ **Accessibility** - WCAG 2.1 AA/AAA compliance  
✅ **Caption Quality** - WER, latency, accuracy metrics  
✅ **Compliance** - FCC and ADA regulatory testing  
✅ **Reporting** - HTML, JSON, and metrics reports  

## Next Steps

1. Review `SETUP.md` for detailed setup instructions
2. Check `ARCHITECTURE.md` for framework design
3. Read `CONTRIBUTING.md` for adding new tests
4. Customize `config/config.yaml` for your environment

## Getting Help

- Check existing test files for examples
- Review framework utilities in `framework/utils/`
- See page objects in `framework/pages/`
