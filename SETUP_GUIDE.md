# mHWC Automation - Test Case 782 Setup Guide

## Test Case Details
**Test Case ID:** 782  
**Title:** Verify login with valid credentials  
**Module:** Login  
**Type:** Regression (Positive)  
**Severity:** Major  
**Priority:** High  

### Description
User should login successfully using valid credentials

### Preconditions
- User is on login page
- Valid username & password are available

### Test Data
- **URL:** https://uatamrit.piramalswasthya.org/aam/
- **Username:** mokrong
- **Password:** Test@123

---

## Project Structure

```
mHWC-Automation/
├── pages/
│   ├── __init__.py
│   ├── login_page.py           # Page Object Model for Login
│   └── login.ts                # (Existing TypeScript file)
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest configuration
│   ├── base_test.py            # Base test class
│   └── test_login_782.py       # Test Case 782
├── utils/
│   ├── __init__.py
│   └── appium_utils.py         # Utility functions
├── testdata/
│   └── AAM-Regression.json     # Test data
├── logs/                        # Test execution logs (auto-created)
├── screenshots/                 # Test screenshots (auto-created)
├── requirements.txt
└── README.md
```

---

## Prerequisites

### 1. System Requirements
- Python 3.8 or higher
- Android Device/Emulator with Android 8.0 or higher
- Appium Server installed and running
- Node.js (optional, for Appium)

### 2. Install Appium Server

#### Option A: Using npm
```bash
npm install -g appium
npm install -g appium-doctor
appium-doctor  # Verify installations
appium         # Start Appium server
```

#### Option B: Using Python
```bash
pip install appium
```

### 3. Android Setup
Make sure you have:
- Android SDK installed (with platform tools)
- Environment variables set:
  - `ANDROID_HOME` pointing to Android SDK directory
  - `PATH` including `ANDROID_HOME/platform-tools`

---

## Installation Steps

### Step 1: Clone/Set up the Project
```bash
cd "c:\Users\Archita Verma\OneDrive - PIRAMAL SWASTHYA MANAGEMENT AND RESEARCH INSTITUTE\AUTOMATION\mHWC-Automation"
```

### Step 2: Create Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Appium Settings

The Appium capabilities are already configured with your Inspector settings:

```json
{
  "platformName": "Android",
  "appium:deviceName": "emulator-5554",
  "appium:automationName": "UiAutomator2",
  "appium:appPackage": "org.piramalswasthya.cho.niramay.uat",
  "appium:appActivity": "org.piramalswasthya.cho.ui.home_activity.HomeActivity",
  "appium:noReset": true
}
```

These values are configured in:
- `tests/base_test.py` - Base configuration class
- `tests/test_login_782.py` - Test case configuration

If you need to change these, update the constants in `tests/base_test.py`

### Step 5: Get Device Information

```bash
# List connected devices
adb devices

# For emulator:
adb -s emulator-5554 shell getprop ro.build.version.release  # Get Android version

# For physical device:
adb -s <device_id> shell getprop ro.build.version.release
```

---

## Prepare App for Testing

### Update Locators in LoginPage POM

The locators in `pages/login_page.py` need to be updated based on your app's actual UI element IDs:

```python
# Inspect the app and get actual locator IDs
USERNAME_FIELD = (AppiumBy.ID, "actual_username_id")
PASSWORD_FIELD = (AppiumBy.ID, "actual_password_id")
LOGIN_BUTTON = (AppiumBy.ID, "actual_login_button_id")
DASHBOARD_ELEMENT = (AppiumBy.ID, "actual_dashboard_id")
ERROR_MESSAGE = (AppiumBy.ID, "actual_error_message_id")
```

#### Method to Find Locators:
1. Use Appium Inspector: `appium-inspector`
2. Use Android Studio Emulator Tools
3. Use UI Automator Viewer: `uiautomatorviewer`

---

## Running Tests

### Prerequisites Before Running Tests:
1. ✅ Appium server running on port 4723
2. ✅ Android device/emulator connected
3. ✅ App installed or accessible
4. ✅ Application on login page
5. ✅ Locators updated in POM

### Option 1: Run Single Test Case
```bash
pytest tests/test_login_782.py::TestLogin782::test_tc_782_verify_login_with_valid_credentials -v -s
```

### Option 2: Run All Tests in File
```bash
pytest tests/test_login_782.py -v -s
```

### Option 3: Run with HTML Report
```bash
pytest tests/test_login_782.py -v --html=report.html --self-contained-html
```

### Option 4: Run with Parallel Execution
```bash
pytest tests/test_login_782.py -v -n 2
```

### Option 5: Run with Timeout
```bash
pytest tests/test_login_782.py -v --timeout=60
```

### Option 6: Run All Tests
```bash
pytest tests/ -v
```

---

## Test Execution Flow

### Test Case 782 Execution Steps:

1. **Setup Phase**
   - Initialize Appium driver
   - Create LoginPage POM instance
   - Load test data

2. **Test Execution**
   - Open application URL
   - Wait for page to load
   - Enter username: "mokrong"
   - Enter password: "Test@123"
   - Click Login button
   - Wait for navigation

3. **Assertion Phase**
   - Verify dashboard is displayed
   - Verify no error message

4. **Teardown Phase**
   - Take final screenshot (if failed)
   - Close driver
   - Clean up resources

---

## Troubleshooting

### Issue 1: Appium Server Not Connecting
```bash
# Check if server is running
http://127.0.0.1:4723/wd/hub/sessions

# Restart server
appium --log-level warn
```

### Issue 2: Device Not Found
```bash
# Check connected devices
adb devices

# Reconnect device
adb kill-server
adb start-server
adb devices
```

### Issue 3: Element Locators Not Working
1. Update locator values in `pages/login_page.py`
2. Use Appium Inspector to inspect actual locators
3. Verify element is visible before clicking

### Issue 4: Element Timeout
Increase timeout in `base_test.py`:
```python
def wait_for_element(self, locator: tuple, timeout: int = 20):  # Increased to 20
```

### Issue 5: Import Errors
```bash
# Ensure Python path is set
export PYTHONPATH="${PYTHONPATH}:/path/to/mHWC-Automation"

# On Windows:
set PYTHONPATH=%PYTHONPATH%;c:\Users\Archita Verma\...\mHWC-Automation
```

---

## Best Practices

1. **Always use Page Object Model** - Maintain locators in POM
2. **Use explicit waits** - Don't rely on implicit waits
3. **Take screenshots** - For debugging failed tests
4. **Log activities** - Check logs for detailed execution info
5. **Clean up resources** - Always close driver in teardown
6. **Use fixtures** - Leverage pytest fixtures for setup/teardown
7. **Data-driven tests** - Use test data from testdata folder

---

## Next Steps

### To Add More Test Cases:
1. Extract test case details from `testdata/AAM-Regression.json`
2. Create new POM classes for new pages (if needed)
3. Create test files in `tests/` folder
4. Follow same structure as `test_login_782.py`

### Example: Create Test Case 783
```bash
# Create pages/registration_page.py POM
# Create tests/test_registration_783.py with TestLogin783 class
pytest tests/test_registration_783.py -v
```

---

## Support & Documentation

### Appium Documentation
- [Appium Official Docs](http://appium.io/docs/en/2.0/)
- [Appium Python Client](https://github.com/appium/python-client)

### Pytest Documentation
- [Pytest Official Docs](https://docs.pytest.org/)
- [Pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)

### Android Testing
- [Android Test Automation](https://developer.android.com/training/testing)
- [UI Automator](https://developer.android.com/training/testing/ui-automator)

---

## Contact & Feedback

For issues or questions regarding test automation, contact the QA team.

---

**Version:** 1.0  
**Created:** 2026-04-20  
**Last Updated:** 2026-04-20
