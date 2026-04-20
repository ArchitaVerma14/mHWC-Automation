"""
Page Object Model for Login Page
Test Case ID: 782 - Verify login with valid credentials
"""

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webelement import WebElement
from typing import Optional


class LoginPage:
    """Page Object Class for Login Page"""

    # Locators - Based on source.xml from Appium Inspector
    USERNAME_FIELD = (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/et_username")
    PASSWORD_FIELD = (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/et_password_hwc")
    LOGIN_BUTTON = (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/btn_nxt")
    REMEMBER_ME_CHECKBOX = (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/cb_remember")
    NHM_LOGO = (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/iv_nhm_logo")  # Login page indicator
    USERNAME_LAYOUT = (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/username_layout")  # Login page container
    
    # Locators for post-login verification (Dashboard/Home Page)
    SEARCH_BAR = (AppiumBy.XPATH, "//*[@hint='Tap here to Search']")  # Search field on dashboard
    HOME_TAB = (AppiumBy.XPATH, "//*[@text='Home']")  # Home tab
    DASHBOARD_TAB = (AppiumBy.XPATH, "//*[@text='Dashboard']")  # Dashboard tab
    CPHC_HEADER = (AppiumBy.XPATH, "//*[@text='CPHC']")  # CPHC header/title
    DRAWER_LAYOUT = (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/drawer_layout")
    ERROR_MESSAGE = (AppiumBy.XPATH, "//*[@text='Invalid credentials' or @text='Error' or contains(@text, 'error')]")
    
    # Locators for location screen (that appears after login)
    LOCATION_TITLE = (AppiumBy.XPATH, "//*[@text='Location']")
    LOCATION_USE_LOCATION_TEXT = (AppiumBy.XPATH, "//*[@text='Use location']")
    LOCATION_BACK_ARROW = (AppiumBy.XPATH, "//*[@content-desc='Back' or @content-desc='back']")
    LOCATION_PERMISSIONS_TEXT = (AppiumBy.XPATH, "//*[contains(@text, 'location permissions')]")
    
    # Locators for exit application dialog
    EXIT_APP_DIALOG = (AppiumBy.XPATH, "//*[@text='Exit Application']")
    EXIT_APP_NO_BUTTON = (AppiumBy.XPATH, "//android.widget.Button[@text='No']")
    EXIT_APP_YES_BUTTON = (AppiumBy.XPATH, "//android.widget.Button[@text='Yes']")

    def __init__(self, driver):
        """
        Initialize LoginPage with WebDriver instance

        Args:
            driver: Appium WebDriver instance
        """
        self.driver = driver

    def enter_username(self, username: str) -> None:
        """
        Enter username in the username field

        Args:
            username: Username to enter
        """
        username_field = self.driver.find_element(*self.USERNAME_FIELD)
        username_field.clear()
        username_field.send_keys(username)

    def enter_password(self, password: str) -> None:
        """
        Enter password in the password field

        Args:
            password: Password to enter
        """
        password_field = self.driver.find_element(*self.PASSWORD_FIELD)
        password_field.clear()
        password_field.send_keys(password)

    def click_login_button(self) -> None:
        """Click the Login button"""
        login_button = self.driver.find_element(*self.LOGIN_BUTTON)
        login_button.click()

    def is_dashboard_displayed(self) -> bool:
        """
        Check if dashboard is displayed after successful login
        
        Checks for elements visible on the post-login dashboard:
        - Home/Dashboard tabs
        - Search bar
        - CPHC header

        Returns:
            bool: True if dashboard is visible, False otherwise
        """
        try:
            # Check if any dashboard element is visible
            home_tab = self.driver.find_element(*self.HOME_TAB)
            search_bar = self.driver.find_element(*self.SEARCH_BAR)
            
            return home_tab.is_displayed() and search_bar.is_displayed()
        except Exception:
            return False

    def is_login_page_displayed(self) -> bool:
        """
        Check if login page is still displayed

        Returns:
            bool: True if login page is visible, False otherwise
        """
        try:
            login_layout = self.driver.find_element(*self.USERNAME_LAYOUT)
            return login_layout.is_displayed()
        except Exception:
            return False

    def is_error_message_displayed(self) -> bool:
        """
        Check if error message is displayed

        Returns:
            bool: True if error message is visible, False otherwise
        """
        try:
            error_msg = self.driver.find_element(*self.ERROR_MESSAGE)
            return error_msg.is_displayed()
        except Exception:
            return False

    def get_error_message_text(self) -> str:
        """
        Get error message text

        Returns:
            str: Error message text
        """
        try:
            error_msg = self.driver.find_element(*self.ERROR_MESSAGE)
            return error_msg.text
        except Exception:
            return ""

    def login(self, username: str, password: str) -> None:
        """
        Perform complete login flow

        Args:
            username: Username to login with
            password: Password to login with
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    def wait_for_login_success(self, timeout: int = 10) -> bool:
        """
        Wait for login to complete by checking if dashboard elements appear

        Args:
            timeout: Timeout in seconds

        Returns:
            bool: True if login was successful, False otherwise
        """
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        try:
            wait = WebDriverWait(self.driver, timeout)
            # Wait for login page to disappear
            wait.until(EC.invisibility_of_element_located(self.USERNAME_LAYOUT))
            # Wait for dashboard elements to appear
            wait.until(EC.presence_of_element_located(self.SEARCH_BAR))
            return True
        except Exception:
            return False

    def get_dashboard_status(self) -> dict:
        """
        Get details of dashboard elements after successful login

        Returns:
            dict: Status of dashboard elements
        """
        status = {
            "home_tab_visible": False,
            "search_bar_visible": False,
            "dashboard_tab_visible": False,
            "cphc_header_visible": False
        }
        
        try:
            status["home_tab_visible"] = self.driver.find_element(*self.HOME_TAB).is_displayed()
        except:
            pass
            
        try:
            status["search_bar_visible"] = self.driver.find_element(*self.SEARCH_BAR).is_displayed()
        except:
            pass
            
        try:
            status["dashboard_tab_visible"] = self.driver.find_element(*self.DASHBOARD_TAB).is_displayed()
        except:
            pass
            
        try:
            status["cphc_header_visible"] = self.driver.find_element(*self.CPHC_HEADER).is_displayed()
        except:
            pass
            
        return status

    def is_location_screen_displayed(self) -> bool:
        """
        Check if location screen is displayed using multiple detection methods

        Returns:
            bool: True if location screen is visible, False otherwise
        """
        try:
            # Method 1: Check for "Location" title
            try:
                location_title = self.driver.find_element(*self.LOCATION_TITLE)
                if location_title.is_displayed():
                    print("   ✓ Detected 'Location' title")
                    return True
            except Exception:
                pass
            
            # Method 2: Check for "Use location" text
            try:
                use_location = self.driver.find_element(*self.LOCATION_USE_LOCATION_TEXT)
                if use_location.is_displayed():
                    print("   ✓ Detected 'Use location' toggle")
                    return True
            except Exception:
                pass
            
            # Method 3: Check for location permissions text
            try:
                permissions = self.driver.find_element(*self.LOCATION_PERMISSIONS_TEXT)
                if permissions.is_displayed():
                    print("   ✓ Detected location permissions text")
                    return True
            except Exception:
                pass
            
            return False
        except Exception:
            return False

    def press_back_button(self) -> bool:
        """
        Press the EMULATOR back button (hardware back key) to dismiss location screen
        This uses the Android back key which is the most reliable method
        
        Returns:
            bool: True if back button was pressed, False otherwise
        """
        import time
        
        try:
            print("   → Pressing EMULATOR BACK BUTTON (Hardware Key Code 4)...")
            # Press the hardware back key (keycode 4 is Android back button)
            self.driver.press_keycode(4)
            time.sleep(1.5)
            print("   ✓ Back button pressed successfully")
            return True
        except Exception as e:
            print(f"   ✗ Failed to press back button: {e}")
            return False

    def handle_exit_app_dialog(self) -> bool:
        """
        Handle exit application dialog by clicking "No" button
        This dialog may appear if back button is pressed

        Returns:
            bool: True if dialog was handled, False if no dialog present
        """
        import time
        try:
            # Check if exit dialog is visible
            try:
                dialog = self.driver.find_element(*self.EXIT_APP_DIALOG)
                if dialog.is_displayed():
                    print("⚠ Exit Application dialog appeared - clicking NO...")
                    time.sleep(0.5)
                    no_button = self.driver.find_element(*self.EXIT_APP_NO_BUTTON)
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

    def handle_location_screen(self, timeout: int = 10) -> bool:
        """
        Handle location screen by pressing emulator back button if it appears
        Uses multiple detection strategies

        Args:
            timeout: Timeout in seconds to wait for location screen

        Returns:
            bool: True if location screen was handled or not present
        """
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        import time
        
        try:
            # First check if location screen is currently displayed
            if self.is_location_screen_displayed():
                print("⚠ Location screen IS currently displayed - pressing back button ONCE...")
                time.sleep(0.5)
                self.press_back_button()
                time.sleep(2)
                
                # Check if exit dialog appeared and handle it
                self.handle_exit_app_dialog()
                return True
            
            # Try to wait for any location screen element to appear
            print("   Waiting for location screen (up to 10 seconds)...")
            wait = WebDriverWait(self.driver, timeout)
            
            try:
                # Try to detect using any of the location screen indicators
                wait.until(EC.presence_of_element_located(self.LOCATION_TITLE))
                print("⚠ Location screen appeared - pressing back button ONCE...")
                self.press_back_button()
                time.sleep(2)
                
                # Check if exit dialog appeared and handle it
                self.handle_exit_app_dialog()
                return True
            except Exception:
                pass
            
            try:
                wait.until(EC.presence_of_element_located(self.LOCATION_USE_LOCATION_TEXT))
                print("⚠ Location screen appeared - pressing back button ONCE...")
                self.press_back_button()
                time.sleep(2)
                
                # Check if exit dialog appeared and handle it
                self.handle_exit_app_dialog()
                return True
            except Exception:
                pass
            
            # No location screen found
            print("   ✓ No location screen detected")
            return True
                
        except Exception as e:
            print(f"   ✗ Unexpected error in location handling: {e}")
            return False
