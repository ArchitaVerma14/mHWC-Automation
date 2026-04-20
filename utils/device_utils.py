"""
Device Utility Functions for Appium Tests
Provides functions to check app installation status and configure Appium accordingly
"""

import subprocess
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
import time


class DeviceUtils:
    """Utility class for device-related operations"""
    
    APP_PACKAGE = "org.piramalswasthya.cho.niramay.uat"
    
    # Location screen locators
    LOCATION_TITLE = (AppiumBy.XPATH, "//*[@text='Location']")
    LOCATION_USE_LOCATION_TEXT = (AppiumBy.XPATH, "//*[@text='Use location']")
    LOCATION_PERMISSIONS_TEXT = (AppiumBy.XPATH, "//*[contains(@text, 'location permissions')]")
    EXIT_APP_DIALOG = (AppiumBy.XPATH, "//*[@text='Exit Application']")
    EXIT_APP_NO_BUTTON = (AppiumBy.XPATH, "//android.widget.Button[@text='No']")
    
    @staticmethod
    def is_app_installed(device_id: str = "emulator-5554") -> bool:
        """
        Check if the app is already installed on the emulator
        
        Args:
            device_id: Device ID (default: emulator-5554)
            
        Returns:
            bool: True if app is installed, False otherwise
        """
        try:
            # Run adb command to check if app is installed
            cmd = ["adb", "-s", device_id, "shell", "pm", "list", "packages"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                # Check if package is in the list
                installed = DeviceUtils.APP_PACKAGE in result.stdout
                status = "✓ INSTALLED" if installed else "✗ NOT INSTALLED"
                print(f"   App Status: {status} on {device_id}")
                return installed
            else:
                print(f"   ✗ Error checking app status: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"   ✗ ADB command timed out")
            return False
        except Exception as e:
            print(f"   ✗ Error checking app installation: {e}")
            return False
    
    @staticmethod
    def get_no_reset_value(device_id: str = "emulator-5554") -> bool:
        """
        Determine the appropriate noReset value based on app installation status
        
        Smart logic:
        - If app is installed: no_reset = True (keep it, faster)
        - If app is not installed: no_reset = False (install it)
        
        Args:
            device_id: Device ID (default: emulator-5554)
            
        Returns:
            bool: noReset value to use
        """
        print("\n" + "="*60)
        print("CHECKING APP INSTALLATION STATUS")
        print("="*60)
        
        is_installed = DeviceUtils.is_app_installed(device_id)
        
        if is_installed:
            no_reset = True
            mode = "KEEP APP (faster, preserves state)"
        else:
            no_reset = False
            mode = "INSTALL APP (clean state)"
        
        print(f"   Mode: {mode}")
        print("="*60 + "\n")
        
        return no_reset
    
    @staticmethod
    def clear_app_data(device_id: str = "emulator-5554") -> bool:
        """
        Clear app data and cache
        
        Args:
            device_id: Device ID (default: emulator-5554)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            cmd = ["adb", "-s", device_id, "shell", "pm", "clear", DeviceUtils.APP_PACKAGE]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print(f"   ✓ App data cleared on {device_id}")
                return True
            else:
                print(f"   ✗ Error clearing app data: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"   ✗ Error clearing app data: {e}")
            return False
    
    @staticmethod
    def uninstall_app(device_id: str = "emulator-5554") -> bool:
        """
        Uninstall the app
        
        Args:
            device_id: Device ID (default: emulator-5554)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            cmd = ["adb", "-s", device_id, "uninstall", DeviceUtils.APP_PACKAGE]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print(f"   ✓ App uninstalled from {device_id}")
                return True
            else:
                print(f"   ✗ Error uninstalling app: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"   ✗ Error uninstalling app: {e}")
            return False
    
    @staticmethod
    def is_location_screen_displayed(driver) -> bool:
        """
        Check if location screen is displayed using multiple detection methods

        Args:
            driver: Appium WebDriver instance

        Returns:
            bool: True if location screen is visible, False otherwise
        """
        try:
            # Method 1: Check for "Location" title
            try:
                location_title = driver.find_element(*DeviceUtils.LOCATION_TITLE)
                if location_title.is_displayed():
                    return True
            except Exception:
                pass
            
            # Method 2: Check for "Use location" text
            try:
                use_location = driver.find_element(*DeviceUtils.LOCATION_USE_LOCATION_TEXT)
                if use_location.is_displayed():
                    return True
            except Exception:
                pass
            
            # Method 3: Check for location permissions text
            try:
                permissions = driver.find_element(*DeviceUtils.LOCATION_PERMISSIONS_TEXT)
                if permissions.is_displayed():
                    return True
            except Exception:
                pass
            
            return False
        except Exception:
            return False
    
    @staticmethod
    def press_back_button(driver) -> bool:
        """
        Press the EMULATOR back button (hardware back key) to dismiss location screen

        Args:
            driver: Appium WebDriver instance

        Returns:
            bool: True if back button was pressed, False otherwise
        """
        try:
            print("   → Pressing EMULATOR BACK BUTTON (Hardware Key Code 4)...")
            driver.press_keycode(4)  # Android back key code
            time.sleep(1.5)
            print("   ✓ Back button pressed successfully")
            return True
        except Exception as e:
            print(f"   ✗ Failed to press back button: {e}")
            return False
    
    @staticmethod
    def handle_exit_app_dialog(driver) -> bool:
        """
        Handle exit application dialog by clicking "No" button

        Args:
            driver: Appium WebDriver instance

        Returns:
            bool: True if dialog was handled, False if no dialog present
        """
        try:
            # Check if exit dialog is visible
            try:
                dialog = driver.find_element(*DeviceUtils.EXIT_APP_DIALOG)
                if dialog.is_displayed():
                    print("⚠ Exit Application dialog appeared - clicking NO...")
                    time.sleep(0.5)
                    no_button = driver.find_element(*DeviceUtils.EXIT_APP_NO_BUTTON)
                    no_button.click()
                    time.sleep(1)
                    print("   ✓ Exit dialog dismissed by clicking NO")
                    return True
            except Exception:
                pass
            return False
        except Exception as e:
            print(f"   ✗ Error handling exit dialog: {e}")
            return False
    
    @staticmethod
    def scroll_up_to_app_drawer(driver) -> bool:
        """
        Scroll up from home screen to show app drawer
        This is needed because automation only works when app drawer is visible
        
        Args:
            driver: Appium WebDriver instance
            
        Returns:
            bool: True if scrolled, False if already on app drawer or error
        """
        try:
            print("   → Scrolling up to show app drawer...")
            
            # Get window size
            window_size = driver.get_window_size()
            width = window_size['width']
            height = window_size['height']
            
            # Swipe up from bottom to top to reveal app drawer
            start_x = width // 2
            start_y = height - 100  # Start from bottom
            end_x = width // 2
            end_y = 100  # End at top
            
            # Perform swipe/scroll
            driver.swipe(start_x, start_y, end_x, end_y, duration=1000)
            time.sleep(1.5)
            
            print("   ✓ Scrolled up to app drawer")
            return True
            
        except Exception as e:
            print(f"   ✗ Error scrolling up: {e}")
            return False
    
    @staticmethod
    def ensure_app_drawer_visible(driver) -> bool:
        """
        Ensure app drawer is visible before proceeding
        Scrolls up if on home screen
        
        Args:
            driver: Appium WebDriver instance
            
        Returns:
            bool: True if app drawer is visible or made visible
        """
        try:
            print("   Checking if app drawer is visible...")
            
            # Try to scroll up multiple times to ensure app drawer is visible
            for attempt in range(3):
                DeviceUtils.scroll_up_to_app_drawer(driver)
                time.sleep(0.5)
            
            print("   ✓ App drawer should be visible now")
            return True
            
        except Exception as e:
            print(f"   ✗ Error ensuring app drawer: {e}")
            return False
    
    @staticmethod
    def launch_app_from_drawer(driver, timeout: int = 10) -> bool:
        """
        Click on the app icon in the app drawer to launch it
        
        Args:
            driver: Appium WebDriver instance
            timeout: Timeout in seconds to wait for app to load
            
        Returns:
            bool: True if app was launched, False otherwise
        """
        try:
            print("   → Looking for AAM app icon in app drawer...")
            wait = WebDriverWait(driver, timeout)
            
            # Try multiple app name patterns to find the app launcher
            app_locators = [
                (AppiumBy.XPATH, "//*[@text='AAM' or @text='aam' or contains(@text, 'AAM')]"),
                (AppiumBy.XPATH, "//*[contains(@content-desc, 'AAM') or contains(@content-desc, 'aam')]"),
                (AppiumBy.XPATH, "//android.widget.TextView[@text='AAM']"),
                (AppiumBy.ACCESSIBILITY_ID, "AAM"),
            ]
            
            app_element = None
            for locator in app_locators:
                try:
                    print(f"   → Trying locator: {locator[1][:50]}...")
                    app_element = wait.until(EC.presence_of_element_located(locator))
                    if app_element.is_displayed():
                        print(f"   ✓ Found app element")
                        break
                except Exception:
                    continue
            
            if app_element is None:
                print("   ⚠ Could not find AAM app icon, trying to access by package name...")
                # Fallback: Let Appium handle app activation by package
                driver.activate_app(DeviceUtils.APP_PACKAGE)
                time.sleep(3)
                print("   ✓ App activated via package name")
                return True
            
            # Click on the app icon
            print("   → Clicking on app icon...")
            app_element.click()
            time.sleep(3)  # Wait for app to launch
            
            print("   ✓ App launched from drawer")
            return True
            
        except Exception as e:
            print(f"   ✗ Error launching app from drawer: {e}")
            # Try fallback method
            try:
                print("   → Trying fallback: activating app via package name...")
                driver.activate_app(DeviceUtils.APP_PACKAGE)
                time.sleep(3)
                print("   ✓ App activated via package name (fallback)")
                return True
            except Exception as e2:
                print(f"   ✗ Fallback also failed: {e2}")
                return False
    
    @staticmethod
    def handle_location_screen(driver, timeout: int = 10) -> bool:
        """
        Handle location screen by pressing emulator back button if it appears
        Also handles exit application dialog if triggered by back button

        Args:
            driver: Appium WebDriver instance
            timeout: Timeout in seconds to wait for location screen

        Returns:
            bool: True if location screen was handled or not present
        """
        try:
            # First check if location screen is currently displayed
            if DeviceUtils.is_location_screen_displayed(driver):
                print("⚠ Location screen IS currently displayed - pressing back button ONCE...")
                time.sleep(0.5)
                DeviceUtils.press_back_button(driver)
                time.sleep(2)
                
                # Check if exit dialog appeared and handle it
                DeviceUtils.handle_exit_app_dialog(driver)
                return True
            
            # Try to wait for any location screen element to appear
            print("   Waiting for location screen (up to 10 seconds)...")
            wait = WebDriverWait(driver, timeout)
            
            try:
                # Try to detect using any of the location screen indicators
                wait.until(EC.presence_of_element_located(DeviceUtils.LOCATION_TITLE))
                print("⚠ Location screen appeared - pressing back button ONCE...")
                DeviceUtils.press_back_button(driver)
                time.sleep(2)
                
                # Check if exit dialog appeared and handle it
                DeviceUtils.handle_exit_app_dialog(driver)
                return True
            except Exception:
                pass
            
            try:
                wait.until(EC.presence_of_element_located(DeviceUtils.LOCATION_USE_LOCATION_TEXT))
                print("⚠ Location screen appeared - pressing back button ONCE...")
                DeviceUtils.press_back_button(driver)
                time.sleep(2)
                
                # Check if exit dialog appeared and handle it
                DeviceUtils.handle_exit_app_dialog(driver)
                return True
            except Exception:
                pass
            
            # No location screen found
            print("   ✓ No location screen detected")
            return True
                
        except Exception as e:
            print(f"   ✗ Unexpected error in location handling: {e}")
            return False
