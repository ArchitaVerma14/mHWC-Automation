"""
Test Case 783: Verify login with invalid credentials
Module: Login
Test Type: Regression (Negative)
Severity: Major
Priority: High

Description: Check system behavior for invalid login
Preconditions: User must be on Login page
Postconditions: System should not allow access to the dashboard
"""

import pytest
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from pages.login_page import LoginPage
from utils.device_utils import DeviceUtils


class TestLogin783:
    """Test Class for Login TC-783 - Invalid Credentials"""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """
        Setup and Teardown for each test

        Sets up Appium driver and initializes LoginPage object
        Tears down the driver after test completion
        """
        # Configure Appium options with UiAutomator2Options
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.device_name = "emulator-5554"
        options.automation_name = "UiAutomator2"
        options.app = "C:/Users/Archita Verma/OneDrive - PIRAMAL SWASTHYA MANAGEMENT AND RESEARCH INSTITUTE/Desktop/APK files/AAM.apk"
        options.auto_grant_permissions = True
        options.no_reset = DeviceUtils.get_no_reset_value("emulator-5554")  # Smart value

        # Initialize Appium driver
        self.driver = webdriver.Remote(
            "http://127.0.0.1:4723",
            options=options
        )

        # IMPORTANT: Scroll up to show app drawer
        # Automation only works when app drawer is visible, not on home screen
        print("\n✓ Ensuring app drawer is visible for automation...")
        DeviceUtils.ensure_app_drawer_visible(self.driver)
        
        # Wait for app to launch
        time.sleep(3)

        # Initialize LoginPage object
        self.login_page = LoginPage(self.driver)

        yield

        # Teardown
        if self.driver:
            self.driver.quit()

    def test_tc_783_verify_login_with_invalid_credentials(self):
        """
        Test Case: 783 - Verify login with invalid credentials

        This test automatically:
        1. Launches the application
        2. Enters invalid username (invalid_user)
        3. Enters invalid password (invalid@123)
        4. Clicks Login button
        5. Verifies login failure and error handling

        Expected Result:
        1. System should display proper error message
        2. User should not be logged in
        3. Dashboard should not be accessible
        """

        print("\n" + "="*70)
        print("TEST CASE 783: Verify Login with Invalid Credentials (Negative Test)")
        print("="*70)
        
        # Step 1: App is already launched by Appium
        print("✓ Step 1: Application launched")
        time.sleep(1)
        
        # Check for location screen (can appear anytime)
        DeviceUtils.handle_location_screen(self.driver, timeout=2)

        # Step 2: Enter invalid username
        invalid_username = "invalid_user"
        print(f"✓ Step 2: Entering invalid username: {invalid_username}")
        self.login_page.enter_username(invalid_username)
        time.sleep(1)
        
        # Check for location screen (can appear anytime)
        DeviceUtils.handle_location_screen(self.driver, timeout=2)

        # Step 3: Enter invalid password
        invalid_password = "invalid@123"
        print(f"✓ Step 3: Entering invalid password: ***")
        self.login_page.enter_password(invalid_password)
        time.sleep(1)
        
        # Check for location screen (can appear anytime)
        DeviceUtils.handle_location_screen(self.driver, timeout=2)

        # Step 4: Click Login button
        print("✓ Step 4: Clicking Login button")
        self.login_page.click_login_button()
        time.sleep(2)
        
        # Check for location screen (can appear anytime)
        DeviceUtils.handle_location_screen(self.driver, timeout=2)

        # Step 5: Verify login failed
        print("✓ Step 5: Verifying login failure handling...")
        
        # Check if login page is still visible (login failed)
        login_page_still_visible = self.login_page.is_login_page_displayed()
        has_error_message = self.login_page.is_error_message_displayed()
        
        print(f"   - Login page still visible: {login_page_still_visible}")
        print(f"   - Error message displayed: {has_error_message}")
        
        # Check for location screen before assertions
        DeviceUtils.handle_location_screen(self.driver, timeout=2)
        
        # At least one of these should be true for a failed login
        assert login_page_still_visible or has_error_message, \
            "Login should fail: page should remain visible or error message should be displayed"

        # Step 6: Verify dashboard should NOT be accessible
        print("✓ Step 6: Verifying dashboard is NOT accessible")
        
        # Check for location screen before verification
        DeviceUtils.handle_location_screen(self.driver, timeout=2)
        
        dashboard_displayed = self.login_page.is_dashboard_displayed()
        dashboard_status = self.login_page.get_dashboard_status()
        
        print(f"   - Dashboard accessible: {dashboard_displayed}")
        print(f"   - Dashboard status: {dashboard_status}")
        
        # Dashboard should NOT be displayed
        assert not dashboard_displayed, \
            "Dashboard should not be accessible with invalid credentials"

        # Step 7: Display error message if available
        if has_error_message:
            error_text = self.login_page.get_error_message_text()
            print(f"✓ Step 7: Error message displayed: {error_text}")
        
        # Final check for location screen
        DeviceUtils.handle_location_screen(self.driver, timeout=2)

        print("\n" + "="*70)
        print("✓✓✓ TEST CASE 783 PASSED ✓✓✓")
        print("Invalid credentials properly rejected")
        print("System prevents unauthorized access to dashboard")
        print("="*70 + "\n")


if __name__ == "__main__":
    # Run tests using pytest
    # Command: pytest tests/test_login_783.py -v -s
    pytest.main([__file__, "-v", "-s"])
