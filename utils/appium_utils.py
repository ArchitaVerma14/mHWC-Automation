"""
Utility functions for test automation
"""

import time
import logging
from typing import Optional, Tuple
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)


class AppiumUtils:
    """Utility class for Appium operations"""

    @staticmethod
    def wait_and_find_element(
        driver: WebDriver,
        locator: Tuple,
        timeout: int = 10,
        poll_frequency: float = 0.2
    ) -> Optional[WebElement]:
        """
        Wait for element to be present and return it

        Args:
            driver: Appium WebDriver instance
            locator: Tuple of (By, value)
            timeout: Timeout in seconds
            poll_frequency: How often to poll for element

        Returns:
            WebElement if found, None otherwise
        """
        try:
            wait = WebDriverWait(driver, timeout, poll_frequency=poll_frequency)
            element = wait.until(EC.presence_of_element_located(locator))
            logger.info(f"Element found: {locator}")
            return element
        except TimeoutException:
            logger.warning(f"Element not found within {timeout} seconds: {locator}")
            return None

    @staticmethod
    def wait_and_click_element(
        driver: WebDriver,
        locator: Tuple,
        timeout: int = 10
    ) -> bool:
        """
        Wait for element to be clickable and click it

        Args:
            driver: Appium WebDriver instance
            locator: Tuple of (By, value)
            timeout: Timeout in seconds

        Returns:
            bool: True if clicked, False otherwise
        """
        try:
            wait = WebDriverWait(driver, timeout)
            element = wait.until(EC.element_to_be_clickable(locator))
            element.click()
            logger.info(f"Element clicked: {locator}")
            return True
        except TimeoutException:
            logger.error(f"Element not clickable within {timeout} seconds: {locator}")
            return False

    @staticmethod
    def wait_and_send_keys(
        driver: WebDriver,
        locator: Tuple,
        text: str,
        timeout: int = 10,
        clear_first: bool = True
    ) -> bool:
        """
        Wait for element and send text to it

        Args:
            driver: Appium WebDriver instance
            locator: Tuple of (By, value)
            text: Text to send
            timeout: Timeout in seconds
            clear_first: Whether to clear field before sending text

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            element = AppiumUtils.wait_and_find_element(driver, locator, timeout)
            if element:
                if clear_first:
                    element.clear()
                element.send_keys(text)
                logger.info(f"Text sent to element: {locator}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error sending text to element {locator}: {str(e)}")
            return False

    @staticmethod
    def get_element_text(
        driver: WebDriver,
        locator: Tuple,
        timeout: int = 10
    ) -> Optional[str]:
        """
        Get text from element

        Args:
            driver: Appium WebDriver instance
            locator: Tuple of (By, value)
            timeout: Timeout in seconds

        Returns:
            str: Element text, None if not found
        """
        try:
            element = AppiumUtils.wait_and_find_element(driver, locator, timeout)
            if element:
                text = element.text
                logger.info(f"Text retrieved from element {locator}: {text}")
                return text
            return None
        except Exception as e:
            logger.error(f"Error getting text from element {locator}: {str(e)}")
            return None

    @staticmethod
    def is_element_displayed(
        driver: WebDriver,
        locator: Tuple,
        timeout: int = 5
    ) -> bool:
        """
        Check if element is displayed

        Args:
            driver: Appium WebDriver instance
            locator: Tuple of (By, value)
            timeout: Timeout in seconds

        Returns:
            bool: True if displayed, False otherwise
        """
        try:
            wait = WebDriverWait(driver, timeout)
            element = wait.until(EC.visibility_of_element_located(locator))
            logger.info(f"Element is displayed: {locator}")
            return True
        except TimeoutException:
            logger.warning(f"Element not visible within {timeout} seconds: {locator}")
            return False

    @staticmethod
    def wait_for_navigation(
        driver: WebDriver,
        timeout: int = 10
    ) -> None:
        """
        Wait for page/navigation to complete

        Args:
            driver: Appium WebDriver instance
            timeout: Timeout in seconds
        """
        try:
            wait = WebDriverWait(driver, timeout)
            wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
            logger.info("Navigation completed")
        except Exception as e:
            logger.warning(f"Navigation wait error: {str(e)}")
            time.sleep(2)  # Fallback to timeout

    @staticmethod
    def take_screenshot(
        driver: WebDriver,
        filename: str
    ) -> bool:
        """
        Take screenshot

        Args:
            driver: Appium WebDriver instance
            filename: Screenshot filename with path

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            driver.save_screenshot(filename)
            logger.info(f"Screenshot saved: {filename}")
            return True
        except Exception as e:
            logger.error(f"Error taking screenshot: {str(e)}")
            return False

    @staticmethod
    def switch_to_context(
        driver: WebDriver,
        context_name: str
    ) -> bool:
        """
        Switch to different context (WEB/NATIVE)

        Args:
            driver: Appium WebDriver instance
            context_name: Context name (e.g., 'WEBVIEW_<package>')

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            driver.switch_to.context(context_name)
            logger.info(f"Switched to context: {context_name}")
            return True
        except Exception as e:
            logger.error(f"Error switching context: {str(e)}")
            return False


class TestDataUtils:
    """Utility class for test data management"""

    VALID_CREDENTIALS = {
        "username": "mokrong",
        "password": "Test@123"
    }

    INVALID_CREDENTIALS = {
        "username": "invaliduser",
        "password": "invalidpass"
    }

    @staticmethod
    def get_valid_credentials() -> dict:
        """Get valid login credentials"""
        return TestDataUtils.VALID_CREDENTIALS.copy()

    @staticmethod
    def get_invalid_credentials() -> dict:
        """Get invalid login credentials"""
        return TestDataUtils.INVALID_CREDENTIALS.copy()
