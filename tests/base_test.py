"""
Base Test Class for all test cases
Provides common setup and teardown functionality
"""

import pytest
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from typing import Optional
from utils.device_utils import DeviceUtils


class BaseTest:
    """Base test class with common setup and teardown"""

    # Appium capabilities
    PLATFORM_NAME = "Android"
    DEVICE_NAME = "emulator-5554"
    APP_PATH = r"C:\Users\Archita Verma\OneDrive - PIRAMAL SWASTHYA MANAGEMENT AND RESEARCH INSTITUTE\Desktop\APK files\AAM.apk"
    AUTOMATION_NAME = "UiAutomator2"
    APPIUM_SERVER_URL = "http://127.0.0.1:4723"

    def __init__(self):
        """Initialize BaseTest"""
        self.driver = None

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """
        Setup and Teardown fixture for all tests

        Initializes Appium driver before each test
        Closes driver after each test
        """
        self.setup()
        yield
        self.teardown()

    def setup(self):
        """
        Setup method to initialize driver with UiAutomator2Options
        
        Automatically determines whether to install or keep existing APK:
        - If app is installed: no_reset=True (faster, keeps app)
        - If app is not installed: no_reset=False (installs fresh)
        """
        # Check if app is installed and determine no_reset value
        no_reset_value = DeviceUtils.get_no_reset_value(self.DEVICE_NAME)
        
        # Create UiAutomator2Options for Android automation
        options = UiAutomator2Options()
        
        # Set basic capabilities
        options.platform_name = self.PLATFORM_NAME
        options.device_name = self.DEVICE_NAME
        options.automation_name = self.AUTOMATION_NAME
        options.app = self.APP_PATH  # APK path - will auto-install if needed
        
        # Set behavior options
        options.auto_grant_permissions = True  # Auto-grant app permissions
        options.no_reset = no_reset_value  # Smart value based on app installation status
        
        print(f"\n{'='*60}")
        print("APPIUM DRIVER SETUP")
        print(f"{'='*60}")
        print(f"✓ Platform: {self.PLATFORM_NAME}")
        print(f"✓ Device: {self.DEVICE_NAME}")
        print(f"✓ Automation: {self.AUTOMATION_NAME}")
        print(f"✓ APK Path: {self.APP_PATH}")
        print(f"✓ Auto-Grant Permissions: True")
        print(f"✓ noReset (Smart mode): {no_reset_value}")
        print(f"✓ Server URL: {self.APPIUM_SERVER_URL}")
        print(f"{'='*60}\n")

        # Initialize the driver
        self.driver = webdriver.Remote(
            self.APPIUM_SERVER_URL,
            options=options
        )
        
        # IMPORTANT: Scroll up to show app drawer
        # Automation only works when app drawer is visible, not on home screen
        print("✓ Ensuring app drawer is visible for automation...")
        DeviceUtils.ensure_app_drawer_visible(self.driver)
        
        # Launch the app by clicking on it in the app drawer
        print("✓ Launching app from drawer...")
        DeviceUtils.launch_app_from_drawer(self.driver)
        
        print("✓ Appium Driver Initialized Successfully\n")

    def teardown(self):
        """Teardown method to close driver"""
        if self.driver:
            self.driver.quit()

    def wait_for_element(self, locator: tuple, timeout: int = 10) -> bool:
        """
        Wait for element to be present and visible

        Args:
            locator: Tuple of (By, value)
            timeout: Timeout in seconds

        Returns:
            bool: True if element is found, False otherwise
        """
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except Exception:
            return False

    def click_element(self, locator: tuple) -> None:
        """
        Click on element

        Args:
            locator: Tuple of (By, value)
        """
        element = self.driver.find_element(*locator)
        element.click()

    def send_keys_to_element(self, locator: tuple, text: str) -> None:
        """
        Send text to element

        Args:
            locator: Tuple of (By, value)
            text: Text to send
        """
        element = self.driver.find_element(*locator)
        element.clear()
        element.send_keys(text)

    def get_element_text(self, locator: tuple) -> str:
        """
        Get text from element

        Args:
            locator: Tuple of (By, value)

        Returns:
            str: Element text
        """
        element = self.driver.find_element(*locator)
        return element.text

    def is_element_displayed(self, locator: tuple) -> bool:
        """
        Check if element is displayed

        Args:
            locator: Tuple of (By, value)

        Returns:
            bool: True if element is displayed, False otherwise
        """
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except Exception:
            return False

    def take_screenshot(self, filename: str) -> None:
        """
        Take screenshot

        Args:
            filename: Screenshot filename
        """
        self.driver.save_screenshot(f"screenshots/{filename}")
