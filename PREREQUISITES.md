# Prerequisites Checklist for Test Execution

## Before Running Tests - Verify All Items:

### 1. Appium Server Running
```powershell
# Terminal 1: Start Appium Server
appium --log-level warn

# Expected output: [Appium] Appium REST http server listening on http://127.0.0.1:4723
```

### 2. Android Emulator/Device Connected
```powershell
# Terminal 2: Verify Emulator
adb devices

# Expected output:
# emulator-5554   device
```

### 3. Application Installed
```powershell
# Check if app is installed
adb shell pm list packages | findstr "piramalswasthya"

# Expected output:
# package:org.piramalswasthya.cho.niramay.uat
```

### 4. Virtual Environment Activated
```powershell
# If not already activated, run:
.\venv\Scripts\Activate.ps1

# OR use python directly from venv:
.\venv\Scripts\pytest.exe tests/test_login_782.py -v -s
```

### 5. Dependencies Installed
```powershell
# Verify all dependencies are installed
.\venv\Scripts\pip.exe list | findstr pytest

# Expected: pytest version 9.0.0 or higher
```

---

## Running the Test

### Option A: Using Virtual Environment Python (Recommended)
```powershell
cd "c:\Users\Archita Verma\OneDrive - PIRAMAL SWASTHYA MANAGEMENT AND RESEARCH INSTITUTE\AUTOMATION\mHWC-Automation"

.\venv\Scripts\pytest.exe tests/test_login_782.py -v -s
```

### Option B: Using System Python (After Activation)
```powershell
.\venv\Scripts\Activate.ps1
pytest tests/test_login_782.py -v -s
```

---

## Troubleshooting

### Emulator Not Running
```powershell
# Start Android emulator
emulator -avd <AVD_NAME>

# List available AVDs
emulator -list-avds
```

### Appium Server Not Starting
```powershell
# Install Appium globally
npm install -g appium

# Install UiAutomator2 driver
appium driver install uiautomator2

# Start Appium
appium --log-level warn
```

### ADB Not Found
- Set ANDROID_HOME environment variable
- Add ANDROID_HOME/platform-tools to PATH
- Restart terminal

### Element Locators Needs Update
If app UI changes, use Appium Inspector:
```
appium-inspector
```
Then update locators in `pages/login_page.py`

---

## Test Execution Flow

1. Appium Server connects to emulator
2. App launches automatically with HomeActivity
3. Login page loads
4. Test enters credentials
5. Test verifies login success/failure
6. Test closes the app

---

## Success Indicators

✅ Test passes if:
- Login page appears
- Credentials are entered without errors
- Login button is clicked successfully
- Dashboard/drawer layout appears after login
- No error messages are shown

❌ Test fails if:
- Cannot connect to Appium server
- Emulator is not available
- App package not found
- Element locators fail to find login fields
- Login times out
