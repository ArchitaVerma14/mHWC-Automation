"""
Test Case 782: Verify login with valid credentials
Module: Login
Test Type: Regression (Positive)
Severity: Major
Priority: High

Description: User should login successfully using valid credentials
Preconditions: User is on login page and has valid username & password
Postconditions: User should be logged in and dashboard should be visible
"""

import pytest
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from pages.login_page import LoginPage
from utils.device_utils import DeviceUtils


class TestLogin782:
    """Test Class for Login TC-782"""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """
        Setup and Teardown for each test

        Sets up Appium driver and initializes LoginPage object
        Tears down the driver after test completion
        """
        self.username = "mokrong"
        self.password = "Test@123"

        # Check app installation status and determine no_reset value
        no_reset_value = DeviceUtils.get_no_reset_value("emulator-5554")

        # Configure Appium options with UiAutomator2Options
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.device_name = "emulator-5554"
        options.automation_name = "UiAutomator2"
        options.app = r"C:\Users\Archita Verma\OneDrive - PIRAMAL SWASTHYA MANAGEMENT AND RESEARCH INSTITUTE\Desktop\APK files\AAM.apk"
        options.auto_grant_permissions = True
        options.no_reset = no_reset_value  # Smart value based on app installation

        # Initialize Appium driver
        self.driver = webdriver.Remote(
            "http://127.0.0.1:4723",
            options=options
        )
        
        # IMPORTANT: Scroll up to show app drawer
        # Automation only works when app drawer is visible, not on home screen
        print("\n✓ Ensuring app drawer is visible for automation...")
        DeviceUtils.ensure_app_drawer_visible(self.driver)
        
        # Launch the app by clicking on it in the app drawer
        print("✓ Launching app from drawer...")
        DeviceUtils.launch_app_from_drawer(self.driver)
        
        # Wait for app to launch
        time.sleep(2)

        # Wait for app to launch
        time.sleep(3)

        # Initialize LoginPage object
        self.login_page = LoginPage(self.driver)

        yield

        # Teardown
        if self.driver:
            self.driver.quit()

    def test_tc_782_verify_login_with_valid_credentials(self):
        """
        Test Case: 782 - Verify login with valid credentials

        This test automatically:
        1. Launches the application
        2. Enters valid username (mokrong)
        3. Enters valid password (Test@123)
        4. Clicks Login button
        5. Verifies successful login

        Expected Result:
        User should be successfully logged in and dashboard should be displayed
        """

        print("\n" + "="*60)
        print("TEST CASE 782: Verify Login with Valid Credentials")
        print("="*60)
        
        # Step 1: App is already launched by Appium
        print("✓ Step 1: Application launched")
        time.sleep(1)
        
        # Check for location screen at any time (can appear anytime)
        DeviceUtils.handle_location_screen(self.driver, timeout=2)

        # Step 2: Enter valid username
        print("✓ Step 2: Entering username: " + self.username)
        self.login_page.enter_username(self.username)
        time.sleep(1)
        
        # Check for location screen (can appear anytime)
        DeviceUtils.handle_location_screen(self.driver, timeout=2)

        # Step 3: Enter valid password
        print("✓ Step 3: Entering password: ***")
        self.login_page.enter_password(self.password)
        time.sleep(1)
        
        # Check for location screen (can appear anytime)
        DeviceUtils.handle_location_screen(self.driver, timeout=2)

        # Step 4: Click Login button
        print("✓ Step 4: Clicking Login button")
        self.login_page.click_login_button()
        time.sleep(3)  # Wait for page to transition
        
        # Check for location screen (can appear anytime)
        DeviceUtils.handle_location_screen(self.driver, timeout=2)

        # Step 5: Take screenshot to see current state
        print("✓ Step 5: Taking screenshot of current screen state...")
        self.driver.save_screenshot("screenshots/after_login_click.png")
        print("   Screenshot saved: screenshots/after_login_click.png")
        time.sleep(1)
        
        # Check for location screen (can appear anytime)
        DeviceUtils.handle_location_screen(self.driver, timeout=2)

        # Step 5.1: Handle location screen if it appears
        print("✓ Step 5.1: Checking and handling location screen if present...")
        location_handled = DeviceUtils.handle_location_screen(self.driver, timeout=10)
        if location_handled:
            print("   ✓ Location screen was handled")
        else:
            print("   ✓ No location screen found")

        # Step 5.2: Wait for login to complete
        print("✓ Step 5.2: Waiting for login page to disappear...")
        login_success = self.login_page.wait_for_login_success(timeout=20)
        
        if not login_success:
            # Take screenshot for debugging
            self.driver.save_screenshot("screenshots/login_failed.png")
            print("   ✗ Login page did not disappear or dashboard did not appear")
            print("   Screenshot saved: screenshots/login_failed.png")
            
        assert login_success, "Login page did not disappear. Login might have failed."

        # Step 6: Verify dashboard is displayed
        print("✓ Step 6: Verifying dashboard is displayed (Home tab, Search bar)")
        time.sleep(2)
        
        # Check for location screen (can appear anytime during verification)
        DeviceUtils.handle_location_screen(self.driver, timeout=2)
        
        # Get dashboard status
        dashboard_status = self.login_page.get_dashboard_status()
        print(f"   Dashboard Status: {dashboard_status}")
        
        dashboard_displayed = self.login_page.is_dashboard_displayed()
        
        if not dashboard_displayed:
            # Take screenshot for debugging
            self.driver.save_screenshot("screenshots/dashboard_not_found.png")
            
        assert dashboard_displayed, "Dashboard is not displayed after login. Home tab and search bar should be visible."

        # Step 7: Additional verifications
        print("✓ Step 7: Verifying dashboard elements...")
        
        # Check for location screen before assertions
        DeviceUtils.handle_location_screen(self.driver, timeout=2)
        
        assert dashboard_status["home_tab_visible"], "Home tab should be visible"
        assert dashboard_status["search_bar_visible"], "Search bar should be visible"
        
        # Step 8: Verify no error message
        print("✓ Step 8: Verifying no error message is shown")
        
        # Check for location screen before final verification
        DeviceUtils.handle_location_screen(self.driver, timeout=2)
        
        has_error = self.login_page.is_error_message_displayed()
        assert not has_error, "Error message should not be displayed on successful login"
        
        # Final check for location screen before declaring success
        DeviceUtils.handle_location_screen(self.driver, timeout=2)

        print("\n" + "="*60)
        print("✓✓✓ TEST CASE 782 PASSED ✓✓✓")
        print("="*60)
        print("User successfully logged in and dashboard is visible")
        print("="*60 + "\n")

if __name__ == "__main__":
    # Run tests using pytest
    # Command: pytest tests/test_login_782.py -v
    pytest.main([__file__, "-v", "-s"])
