# Testing Framework Documentation

## Overview
Comprehensive automated testing framework for the Campus Event System frontend using pytest.

## Installation

### Install Test Dependencies
```bash
cd frontend_tkinter
pip install -r requirements-dev.txt
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test Categories
```bash
# Unit tests only
pytest tests/unit/ -m unit

# Integration tests
pytest tests/integration/ -m integration

# UI tests
pytest tests/ui/ -m ui

# Skip slow tests
pytest -m "not slow"
```

### Run Specific Test Files
```bash
# Test API client
pytest tests/unit/test_api_client.py

# Test session manager
pytest tests/unit/test_session_manager.py

# Test login flow
pytest tests/integration/test_login_flow.py
```

### Run with Coverage Report
```bash
# Generate coverage report
pytest --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
```

### Run with Verbose Output
```bash
pytest -v

# Extra verbose with test output
pytest -vv -s
```

## Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures and configuration
├── fixtures/
│   └── mock_api_responses.json  # Test data
├── unit/                    # Unit tests
│   ├── test_api_client.py
│   ├── test_session_manager.py
│   ├── test_security.py
│   └── test_error_handler.py
├── integration/             # Integration tests
│   ├── test_login_flow.py
│   ├── test_event_creation.py
│   └── test_booking_flow.py
└── ui/                      # UI tests
    ├── test_components.py
    └── test_pages.py
```

## Writing Tests

### Example Unit Test
```python
import pytest
from utils.api_client import APIClient

class TestAPIClient:
    def test_get_request_success(self, mock_api_client):
        # Arrange
        client = APIClient()
        
        # Act
        result = client.get('events')
        
        # Assert
        assert result is not None
```

### Example Integration Test
```python
@pytest.mark.integration
class TestLoginFlow:
    @patch('utils.api_client.APIClient')
    def test_successful_login(self, mock_api, root):
        # Test complete login workflow
        pass
```

### Using Fixtures
```python
def test_with_sample_data(sample_event, sample_user):
    # Use pre-defined test data
    assert sample_event['id'] == 1
    assert sample_user['role'] == 'STUDENT'
```

## Available Fixtures

### Common Fixtures (from conftest.py)
- `root` - Tkinter root window
- `mock_api_client` - Mocked API client
- `mock_session` - Mocked session manager
- `sample_user` - Sample user data
- `sample_event` - Sample event data
- `sample_events_list` - List of sample events
- `sample_booking` - Sample booking data
- `mock_messagebox` - Mocked message boxes
- `mock_error_handler` - Mocked error handler

## Test Markers

### Mark Tests by Category
```python
@pytest.mark.unit
def test_something():
    pass

@pytest.mark.integration
def test_integration():
    pass

@pytest.mark.slow
def test_slow_operation():
    pass

@pytest.mark.requires_backend
def test_with_backend():
    pass
```

## Coverage Goals

- **Target Coverage:** 80%+
- **Critical Modules:** 90%+
  - utils/api_client.py
  - utils/session_manager.py
  - utils/security.py
  - utils/error_handler.py

## Continuous Integration

### GitHub Actions (Future)
```yaml
name: Frontend Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd frontend_tkinter
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: |
          cd frontend_tkinter
          pytest --cov=. --cov-report=xml
```

## Troubleshooting

### Tests Not Discovered
```bash
# Make sure you're in the right directory
cd frontend_tkinter

# Check pytest can find tests
pytest --collect-only
```

### Import Errors
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Check PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

### Tkinter Tests Failing
```bash
# Tkinter tests need display (X11)
# On Linux/macOS, tests auto-hide windows
# On headless systems, use Xvfb:
xvfb-run pytest
```

## Best Practices

1. **Arrange-Act-Assert Pattern**
   ```python
   def test_example():
       # Arrange - Set up test data
       data = {"key": "value"}
       
       # Act - Perform action
       result = function_under_test(data)
       
       # Assert - Verify result
       assert result == expected
   ```

2. **Use Descriptive Names**
   ```python
   # Good
   def test_login_with_invalid_credentials_shows_error():
       pass
   
   # Bad
   def test_login():
       pass
   ```

3. **One Assertion Per Test** (when possible)
   ```python
   def test_user_has_correct_email():
       user = get_user()
       assert user['email'] == 'test@example.com'
   
   def test_user_has_correct_role():
       user = get_user()
       assert user['role'] == 'STUDENT'
   ```

4. **Mock External Dependencies**
   ```python
   @patch('requests.get')
   def test_api_call(mock_get):
       mock_get.return_value = Mock(status_code=200)
       # Test your code
   ```

## Running Tests Before Commit

### Manual Check
```bash
# Run full test suite
pytest

# Run with coverage
pytest --cov=. --cov-report=term-missing
```

### Pre-commit Hook (Future)
```bash
# Install pre-commit
pip install pre-commit

# Set up hooks
pre-commit install

# Now tests run automatically before each commit
```

## Status

✅ **Framework Setup:** Complete  
✅ **Unit Tests:** Template ready  
✅ **Integration Tests:** Template ready  
✅ **UI Tests:** Template ready  
🔄 **Coverage:** In Progress  
⏳ **CI/CD:** Planned

## Next Steps

1. Install dependencies: `pip install -r requirements-dev.txt`
2. Run existing tests: `pytest`
3. Add more test cases for each module
4. Increase coverage to 80%+
5. Set up pre-commit hooks
6. Configure CI/CD pipeline
