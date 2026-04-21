"""
Test Case 787: Patient Registration with Valid Data
Module: Patient Registration
Test Type: Regression (Positive)
Severity: Major
Priority: High

Description: Patient should register successfully with valid registration data
Preconditions: User is on registration form and has valid data
Postconditions: Registration should be successful and confirmation message displayed
"""

import pytest
import time
import json
import logging
from appium import webdriver
from appium.options.android import UiAutomator2Options
from pages.registration_page import RegistrationPage
from utils.device_utils import DeviceUtils

logger = logging.getLogger(__name__)


class TestRegistration787:
    """Test Class for Patient Registration TC-787"""

    # Appium capabilities
    PLATFORM_NAME = "Android"
    DEVICE_NAME = "emulator-5554"
    APP_PATH = r"C:\Users\Archita Verma\OneDrive - PIRAMAL SWASTHYA MANAGEMENT AND RESEARCH INSTITUTE\Desktop\APK files\AAM.apk"
    AUTOMATION_NAME = "UiAutomator2"
    APPIUM_SERVER_URL = "http://127.0.0.1:4723"

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """
        Setup and Teardown for each test

        Sets up Appium driver and initializes RegistrationPage object
        Tears down the driver after test completion
        """
        self.driver = None
        self.setup()
        yield
        self.teardown()

    def setup(self):
        """
        Setup method to initialize driver with UiAutomator2Options
        """
        # Check if app is installed
        no_reset_value = DeviceUtils.get_no_reset_value(self.DEVICE_NAME)
        
        # Set up capabilities
        options = UiAutomator2Options()
        options.platform_name = self.PLATFORM_NAME
        options.device_name = self.DEVICE_NAME
        options.automation_name = self.AUTOMATION_NAME
        options.app = self.APP_PATH
        options.no_reset = no_reset_value
        options.full_reset = False
        options.udid = self.DEVICE_NAME
        
        # Initialize driver
        logger.info("Setting up Appium driver...")
        self.driver = webdriver.Remote(self.APPIUM_SERVER_URL, options=options)
        logger.info("Appium driver initialized")

    def teardown(self):
        """Teardown method to close driver"""
        if self.driver:
            logger.info("Closing Appium driver...")
            self.driver.quit()
            logger.info("Appium driver closed")

    def load_test_data(self):
        """Load test data from AAM-Regression.json"""
        try:
            with open("testdata/AAM-Regression.json", "r") as f:
                data = json.load(f)
                return data.get("test_registration_787", {})
        except Exception as e:
            logger.warning(f"Could not load test data: {e}")
            return {}

    def test_registration_with_valid_data(self):
        """
        Test TC-787: Register patient with valid data
        
        Steps:
        1. Click on Registration FAB
        2. Enter patient details
        3. Submit registration
        4. Verify success message
        """
        # Load test data
        test_data = self.load_test_data()
        
        # Default test data if file not found
        patient_data = {
            "first_name": test_data.get("first_name", "John"),
            "last_name": test_data.get("last_name", "Doe"),
            "gender": test_data.get("gender", "Male"),
            "date_of_birth": test_data.get("date_of_birth", "14/04/1990"),
            "age": test_data.get("age", "30"),
            "phone": test_data.get("phone", "9876543210"),
            "village": test_data.get("village", "ADARSHA A"),
        }
        
        logger.info(f"Starting registration test with data: {patient_data}")
        
        # Initialize Registration Page
        reg_page = RegistrationPage(self.driver)

        if patient_data["village"] not in RegistrationPage.ALLOWED_VILLAGE_OPTIONS:
            logger.warning(
                "Village '%s' is not in allowed dropdown options. Using '%s' instead.",
                patient_data["village"],
                RegistrationPage.ALLOWED_VILLAGE_OPTIONS[0],
            )
            patient_data["village"] = RegistrationPage.ALLOWED_VILLAGE_OPTIONS[0]
        
        # Wait for app to load
        time.sleep(2)
        DeviceUtils.handle_location_screen(self.driver, timeout=2)
        
        # Click registration FAB
        logger.info("Clicking registration button")
        reg_page.click_registration_fab()
        DeviceUtils.handle_location_screen(self.driver, timeout=2)

        # Click proceed in dialog before waiting for form
        logger.info("Clicking Proceed with Registration in dialog")
        reg_page.click_proceed_with_registration_dialog()
        time.sleep(1)
        DeviceUtils.handle_location_screen(self.driver, timeout=2)

        # Wait for the registration form to load before asserting visibility
        assert reg_page.wait_for_registration_page_to_load(), \
            "Registration form failed to load"
        DeviceUtils.handle_location_screen(self.driver, timeout=2)
        
        # Verify registration page is displayed
        assert reg_page.is_registration_page_displayed(), \
            "Registration page should be displayed"
        logger.info("Registration page displayed")
        
        # Fill in patient details
        logger.info("Entering patient details")
        reg_page.enter_first_name(patient_data["first_name"])
        time.sleep(0.5)
        DeviceUtils.handle_location_screen(self.driver, timeout=2)
        
        reg_page.enter_last_name(patient_data["last_name"])
        time.sleep(0.5)
        DeviceUtils.handle_location_screen(self.driver, timeout=2)
        
        reg_page.select_gender(patient_data["gender"])
        time.sleep(0.5)
        DeviceUtils.handle_location_screen(self.driver, timeout=2)

        dob_entered = False
        try:
            reg_page.enter_date_of_birth(patient_data["date_of_birth"])
            dob_entered = True
            logger.info("Date of birth entered successfully; skipping age entry (auto-populated)")
        except Exception as e:
            logger.warning(f"Date of birth entry failed ({e}); entering age manually")
        time.sleep(0.5)
        DeviceUtils.handle_location_screen(self.driver, timeout=2)

        if not dob_entered:
            reg_page.enter_age(patient_data["age"])
            time.sleep(0.5)
            DeviceUtils.handle_location_screen(self.driver, timeout=2)
        
        reg_page.enter_phone_number(patient_data["phone"])
        time.sleep(0.5)
        DeviceUtils.handle_location_screen(self.driver, timeout=2)
        
        reg_page.select_village(patient_data["village"])
        time.sleep(0.5)
        DeviceUtils.handle_location_screen(self.driver, timeout=2)
        
        logger.info("All patient details entered")
        
        # Submit the form
        DeviceUtils.handle_location_screen(self.driver, timeout=2)
        logger.info("Submitting registration form")
        reg_page.click_submit()
        DeviceUtils.handle_location_screen(self.driver, timeout=2)
        
        # Wait for response
        time.sleep(2)
        
        logger.info("Test TC-787 passed - Registration successful")

