"""
Page Object Model for Patient Registration Page
Test Case: Patient Registration Flow
"""

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webelement import WebElement
from typing import Optional
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class RegistrationPage:
    """Page Object Class for Patient Registration Page"""

    # Locators - Based on source.xml
    # Header
    HEADER_TEXT = (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/header_text_register_patient")
    HOME_BUTTON = (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/home_button")
    
    # Registration Button (FloatingActionButton on homepage)
    REGISTRATION_FAB = (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/registration")
    
    # Photo Section
    PHOTO_TITLE = (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/tv_title_photo")
    PHOTO_SUBTITLE = (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/tv_sub_title_photo")
    PHOTO_CAPTURE_BTN = (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/iv_img_capture")
    
    # Form Fields
    FIRST_NAME_FIELD = (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/first_name")
    LAST_NAME_FIELD = (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/last_name")
    GENDER_DROPDOWN = (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/gender_dropdown")
    DATE_OF_BIRTH_FIELD = (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/date_of_birth")
    AGE_FIELD = (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/age")
    PHONE_NUMBER_FIELD = (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/phone_no")
    VILLAGE_DROPDOWN = (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/village_dropdown")
    
    # Buttons
    CANCEL_BUTTON = (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/btnCancel")
    SUBMIT_BUTTON = (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/btnSubmit")  # Main submit button
    
    # Success/Error messages
    SUCCESS_MESSAGE = (AppiumBy.XPATH, "//*[contains(@text, 'success') or contains(@text, 'Success') or contains(@text, 'registered')]")
    ERROR_MESSAGE = (AppiumBy.XPATH, "//*[contains(@text, 'error') or contains(@text, 'Error') or contains(@text, 'required')]")
    
    # Dialog buttons
    PROCEED_WITH_REGISTRATION_BTN = (AppiumBy.ID, "android:id/button2")
    SEARCH_BTN = (AppiumBy.ID, "android:id/button1")
    DIALOG_TITLE = (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/alertTitle")

    def __init__(self, driver):
        """
        Initialize RegistrationPage with WebDriver instance

        Args:
            driver: Appium WebDriver instance
        """
        self.driver = driver

    def is_registration_page_displayed(self) -> bool:
        """
        Check if registration page is displayed by verifying the header

        Returns:
            bool: True if registration page is visible, False otherwise
        """
        try:
            header = self.driver.find_element(*self.HEADER_TEXT)
            return header.is_displayed() and "Patient Registration" in header.text
        except Exception:
            return False

    def enter_first_name(self, first_name: str) -> None:
        """
        Enter first name in the first name field

        Args:
            first_name: First name to enter
        """
        field = self.driver.find_element(*self.FIRST_NAME_FIELD)
        field.clear()
        field.send_keys(first_name)

    def enter_last_name(self, last_name: str) -> None:
        """
        Enter last name/surname in the last name field

        Args:
            last_name: Last name to enter
        """
        field = self.driver.find_element(*self.LAST_NAME_FIELD)
        field.clear()
        field.send_keys(last_name)

    def select_gender(self, gender: str) -> None:
        """
        Select gender from the AutoCompleteTextView dropdown
        
        Tries multiple strategies:
        1. Click dropdown and type gender value
        2. Wait for options to appear
        3. Select the matching option

        Args:
            gender: Gender value to select (e.g., 'Male', 'Female', 'Other')
        """
        try:
            # Strategy 1: Clear field and type the gender value
            dropdown = self.driver.find_element(*self.GENDER_DROPDOWN)
            dropdown.click()
            time.sleep(0.5)
            
            # Clear any existing text
            dropdown.clear()
            time.sleep(0.3)
            
            # Type the gender value
            dropdown.send_keys(gender)
            time.sleep(1)
            
            # Look for the option in dropdown
            gender_option = (AppiumBy.XPATH, f"//*[@text='{gender}']")
            try:
                option = self.driver.find_element(*gender_option)
                option.click()
                time.sleep(0.5)
                return
            except Exception as e:
                print(f"  → First strategy failed: {e}, trying alternative...")
        except Exception as e:
            print(f"  → Initial click failed: {e}")
        
        try:
            # Strategy 2: Try with contains text match
            gender_option = (AppiumBy.XPATH, f"//*[contains(@text, '{gender}')]")
            option = self.driver.find_element(*gender_option)
            option.click()
            time.sleep(0.5)
            return
        except Exception as e:
            print(f"  → Second strategy failed: {e}, trying partial match...")
        
        try:
            # Strategy 3: Find all options and match by partial text
            all_options = self.driver.find_elements(AppiumBy.XPATH, "//*[@class='android.widget.TextView']")
            for option in all_options:
                if gender.lower() in option.text.lower():
                    option.click()
                    time.sleep(0.5)
                    return
        except Exception as e:
            print(f"  → Third strategy failed: {e}")
        
        # If all strategies fail, raise error
        raise Exception(f"Could not find and click gender option: {gender}")

    def enter_date_of_birth(self, date: str) -> None:
        """
        Enter date of birth using Android's Material DatePicker (format: DD/MM/YYYY)
        
        Uses the year picker with scrolling to select the correct year, then calendar for day.
        
        Args:
            date: Date of birth in DD/MM/YYYY format (e.g., "17/04/1990")
        
        Example: enter_date_of_birth("17/04/1990") for April 17, 1990
        """
        try:
            # Parse the date
            day, month, year = date.split('/')
            day = int(day)
            month = int(month)
            year = int(year)
            
            print(f"  → Opening date picker for: {day}/{month}/{year}")
            
            # Click the date field to open the date picker
            field = self.driver.find_element(*self.DATE_OF_BIRTH_FIELD)
            field.click()
            time.sleep(1.5)  # Wait for date picker to open
            print(f"  ✓ Date picker opened")
            
            # Step 1: Click on year header to open year picker
            print(f"  → Opening year picker...")
            try:
                year_header = self.driver.find_element(AppiumBy.ID, "android:id/date_picker_header_year")
                year_header.click()
                time.sleep(1)
                print(f"  ✓ Year picker opened")
            except Exception as e:
                print(f"  ⚠ Could not click year header: {e}")
                raise
            
            # Step 2: Scroll in the year picker to find the target year using ScrollView
            print(f"  → Scrolling to find year: {year}")
            year_text = str(year)
            year_found = False
            max_scroll_attempts = 25
            
            # Find the ScrollView that contains the year picker (android:id/animator)
            scroll_view = None
            try:
                scroll_view = self.driver.find_element(AppiumBy.ID, "android:id/animator")
                print(f"  ✓ Found year picker ScrollView (android:id/animator)")
            except Exception as e:
                print(f"  ⚠ Could not find ScrollView with ID android:id/animator: {e}")
                print(f"  → Will use swipe fallback method")
            
            for scroll_attempt in range(max_scroll_attempts):
                try:
                    # Try to find the year element first
                    year_elements = self.driver.find_elements(AppiumBy.XPATH, 
                        f"//android.widget.TextView[@text='{year_text}']")
                    
                    if year_elements:
                        # Year found, click it
                        year_elem = year_elements[0]
                        year_elem.click()
                        time.sleep(0.5)
                        print(f"  ✓ Year {year_text} found and clicked")
                        year_found = True
                        break
                except Exception:
                    pass
                
                # Year not found yet, scroll in the ScrollView
                try:
                    if scroll_view:
                        # Use native scroll action on ScrollView element
                        # Scroll up or down based on target year
                        if year < 2000:
                            # Scroll up (backward) for earlier years
                            self.driver.execute_script(
                                "mobile: scrollGesture",
                                {"elementId": scroll_view.id, "direction": "up", "percent": 0.75}
                            )
                        else:
                            # Scroll down (forward) for later years
                            self.driver.execute_script(
                                "mobile: scrollGesture",
                                {"elementId": scroll_view.id, "direction": "down", "percent": 0.75}
                            )
                    else:
                        # Fallback to swipe on screen
                        if year < 2000:
                            self.driver.swipe(540, 400, 540, 600, duration=300)
                        else:
                            self.driver.swipe(540, 600, 540, 400, duration=300)
                    
                    time.sleep(0.3)
                    
                    if scroll_attempt % 4 == 0:
                        print(f"  → Scrolling attempt {scroll_attempt + 1}/{max_scroll_attempts}")
                except Exception as scroll_error:
                    print(f"  ⚠ Scroll attempt {scroll_attempt + 1} failed: {scroll_error}")
            
            if not year_found:
                raise Exception(f"Year {year_text} not found in picker after {max_scroll_attempts} scroll attempts")
            
            # Step 3: Wait for calendar to load with selected year
            time.sleep(1.5)
            print(f"  → Waiting for calendar to load...")
            
            # Step 4: Select the day from the month_view calendar
            print(f"  → Selecting day: {day}")
            date_found = False
            
            # Try to find date in month_view
            try:
                month_view = self.driver.find_element(AppiumBy.ID, "android:id/month_view")
                date_buttons = month_view.find_elements(AppiumBy.XPATH, ".//android.widget.Button")
                
                for btn in date_buttons:
                    if btn.text.strip() == str(day):
                        btn.click()
                        time.sleep(0.5)
                        print(f"  ✓ Date {day} selected")
                        date_found = True
                        break
            except Exception as e:
                print(f"  ⚠ Could not select from month_view: {e}")
            
            # Fallback: try simple XPath
            if not date_found:
                try:
                    date_button = self.driver.find_element(AppiumBy.XPATH, 
                        f"//android.widget.Button[@text='{day}']")
                    date_button.click()
                    time.sleep(0.5)
                    print(f"  ✓ Date {day} selected (XPath)")
                    date_found = True
                except Exception as e:
                    print(f"  ⚠ Could not find date button {day}: {e}")
            
            # Step 5: Click OK to confirm the date selection
            print(f"  → Confirming date selection...")
            try:
                ok_button = self.driver.find_element(AppiumBy.XPATH, 
                    "//android.widget.Button[@text='OK']")
                ok_button.click()
                time.sleep(1)
                print(f"  ✓ Date confirmed - Set to: {day}/{month}/{year}")
            except Exception as e:
                print(f"  ⚠ Could not find OK button by text, trying ID...")
                try:
                    ok_button = self.driver.find_element(AppiumBy.ID, "android:id/button1")
                    ok_button.click()
                    time.sleep(1)
                    print(f"  ✓ Date confirmed - Set to: {day}/{month}/{year}")
                except Exception as e2:
                    print(f"  ✗ Could not click OK button: {e2}")
                    raise
        
        except Exception as e:
            print(f"  ✗ Error entering date of birth {date}: {e}")
            raise

    def enter_age(self, age: str) -> None:
        """
        Enter age value

        Args:
            age: Age as string
        """
        field = self.driver.find_element(*self.AGE_FIELD)
        field.clear()
        field.send_keys(age)

    def enter_phone_number(self, phone: str) -> None:
        """
        Enter phone number

        Args:
            phone: Phone number to enter
        """
        field = self.driver.find_element(*self.PHONE_NUMBER_FIELD)
        field.clear()
        field.send_keys(phone)

    def select_village(self, village: str) -> None:
        """
        Select village strictly from visible dropdown options.

        If requested village is not found, selects first valid option from popup.

        Args:
            village: Village name to select (e.g., "ACHARAMPUR", "ADARSHA A")
        """
        try:
            print(f"  → Selecting village: {village}")

            # Read current value before selection for validation
            dropdown = self.driver.find_element(*self.VILLAGE_DROPDOWN)
            previous_value = dropdown.text.strip()

            def _open_village_dropdown():
                opened = False
                try:
                    village_arrow = self.driver.find_element(
                        AppiumBy.XPATH,
                        "(//android.widget.ImageButton[@content-desc='Show dropdown menu'])[2]"
                    )
                    village_arrow.click()
                    opened = True
                    print("  ✓ Opened village dropdown via arrow button")
                except Exception:
                    pass

                if not opened:
                    dropdown.click()
                    print("  → Opened village dropdown via field tap (fallback)")

                time.sleep(0.8)

            def _click_with_fallback(elem):
                try:
                    elem.click()
                    return
                except Exception:
                    pass

                # Some dropdowns require gesture tap instead of element click
                try:
                    self.driver.execute_script(
                        "mobile: clickGesture",
                        {"elementId": elem.id}
                    )
                    return
                except Exception:
                    pass

                rect = elem.rect
                center_x = int(rect["x"] + rect["width"] / 2)
                center_y = int(rect["y"] + rect["height"] / 2)
                self.driver.execute_script(
                    "mobile: clickGesture",
                    {"x": center_x, "y": center_y}
                )

            def _collect_options():
                option_xpath_candidates = [
                    "//android.widget.ListView//android.widget.CheckedTextView",
                    "//androidx.recyclerview.widget.RecyclerView//android.widget.CheckedTextView",
                    "//android.widget.CheckedTextView",
                ]

                for xp in option_xpath_candidates:
                    elems = self.driver.find_elements(AppiumBy.XPATH, xp)
                    filtered = []
                    for elem in elems:
                        try:
                            txt = elem.text.strip()
                            if not elem.is_displayed() or not txt:
                                continue
                            if txt.lower() in ["village", "select village", "villages", "village 1"]:
                                continue
                            filtered.append((txt, elem))
                        except Exception:
                            continue
                    if filtered:
                        return filtered
                return []

            last_seen_options = []
            for attempt in range(3):
                _open_village_dropdown()
                options = _collect_options()
                last_seen_options = [txt for txt, _ in options]

                if not options:
                    print(f"  ⚠ No options captured on attempt {attempt + 1}")
                    continue

                # Try exact requested village first
                target_elem = None
                target_text = None
                for txt, elem in options:
                    if txt.lower() == village.lower():
                        target_text = txt
                        target_elem = elem
                        break

                # If requested village is not visible, choose first option different from current value
                if target_elem is None:
                    for txt, elem in options:
                        if txt != previous_value:
                            target_text = txt
                            target_elem = elem
                            break

                if target_elem is None:
                    target_text, target_elem = options[0]

                if target_text.lower() != village.lower():
                    print(f"  ⚠ Requested village not found, selecting available option: '{target_text}'")

                _click_with_fallback(target_elem)
                time.sleep(0.8)

                selected_value = self.driver.find_element(*self.VILLAGE_DROPDOWN).text.strip()
                if selected_value and selected_value.lower() not in ["village", "select village", "village 1"] and selected_value != previous_value:
                    print(f"  ✓ Village selected from dropdown: '{selected_value}'")
                    return

                print(f"  ⚠ Selection not applied on attempt {attempt + 1}, retrying...")

            raise Exception(
                f"Village selection failed after retries. Previous value='{previous_value}', visible options={last_seen_options}"
            )
        
        except Exception as e:
            print(f"  ✗ Error selecting village {village}: {e}")
            raise

    def click_submit(self) -> None:
        """
        Click the Submit button to submit registration form
        """
        submit_btn = self.driver.find_element(*self.SUBMIT_BUTTON)
        submit_btn.click()

    def click_cancel(self) -> None:
        """
        Click the Cancel button to cancel registration
        """
        cancel_btn = self.driver.find_element(*self.CANCEL_BUTTON)
        cancel_btn.click()

    def click_home(self) -> None:
        """
        Click the Home button in the header
        """
        home_btn = self.driver.find_element(*self.HOME_BUTTON)
        home_btn.click()

    def click_registration_fab(self) -> None:
        """
        Click the Registration FloatingActionButton on homepage
        This button opens the patient registration form
        """
        try:
            registration_fab = self.driver.find_element(*self.REGISTRATION_FAB)
            registration_fab.click()
            time.sleep(1.5)
        except Exception as e:
            print(f"Could not click registration FAB: {e}")
            raise

    def click_photo_capture(self) -> None:
        """
        Click on the photo capture button to take a photo
        """
        photo_btn = self.driver.find_element(*self.PHOTO_CAPTURE_BTN)
        photo_btn.click()

    def click_proceed_with_registration_dialog(self) -> None:
        """
        Click the 'Proceed with Registration' button in the dialog
        """
        try:
            proceed_btn = self.driver.find_element(*self.PROCEED_WITH_REGISTRATION_BTN)
            proceed_btn.click()
        except Exception as e:
            print(f"Could not click proceed button: {e}")
            raise

    def click_search_button_dialog(self) -> None:
        """
        Click the 'Search' button in the dialog
        """
        try:
            search_btn = self.driver.find_element(*self.SEARCH_BTN)
            search_btn.click()
        except Exception as e:
            print(f"Could not click search button: {e}")
            raise

    def is_dialog_displayed(self) -> bool:
        """
        Check if the dialog is displayed
        
        Returns:
            bool: True if dialog visible, False otherwise
        """
        try:
            dialog = self.driver.find_element(*self.DIALOG_TITLE)
            return dialog.is_displayed()
        except Exception:
            return False

    def get_first_name_value(self) -> str:
        """
        Get the current value in the first name field

        Returns:
            str: First name value
        """
        field = self.driver.find_element(*self.FIRST_NAME_FIELD)
        return field.get_attribute("text")

    def get_last_name_value(self) -> str:
        """
        Get the current value in the last name field

        Returns:
            str: Last name value
        """
        field = self.driver.find_element(*self.LAST_NAME_FIELD)
        return field.get_attribute("text")

    def get_gender_value(self) -> str:
        """
        Get the selected gender value

        Returns:
            str: Selected gender
        """
        dropdown = self.driver.find_element(*self.GENDER_DROPDOWN)
        return dropdown.get_attribute("text")

    def get_age_value(self) -> str:
        """
        Get the age value

        Returns:
            str: Age value
        """
        field = self.driver.find_element(*self.AGE_FIELD)
        return field.get_attribute("text")

    def get_phone_value(self) -> str:
        """
        Get the phone number value

        Returns:
            str: Phone number
        """
        field = self.driver.find_element(*self.PHONE_NUMBER_FIELD)
        return field.get_attribute("text")

    def is_error_message_displayed(self) -> bool:
        """
        Check if error message is displayed

        Returns:
            bool: True if error message visible, False otherwise
        """
        try:
            error = self.driver.find_element(*self.ERROR_MESSAGE)
            return error.is_displayed()
        except Exception:
            return False

    def get_error_message_text(self) -> str:
        """
        Get the error message text

        Returns:
            str: Error message text
        """
        try:
            error = self.driver.find_element(*self.ERROR_MESSAGE)
            return error.text
        except Exception:
            return "No error message found"

    def is_success_message_displayed(self) -> bool:
        """
        Check if success message is displayed after registration

        Returns:
            bool: True if success message visible, False otherwise
        """
        try:
            success = self.driver.find_element(*self.SUCCESS_MESSAGE)
            return success.is_displayed()
        except Exception:
            return False

    def get_success_message_text(self) -> str:
        """
        Get the success message text

        Returns:
            str: Success message text
        """
        try:
            success = self.driver.find_element(*self.SUCCESS_MESSAGE)
            return success.text
        except Exception:
            return "No success message found"

    def wait_for_registration_success(self, timeout: int = 10) -> bool:
        """
        Wait for successful registration by checking for success message or page change

        Args:
            timeout: Timeout in seconds

        Returns:
            bool: True if registration was successful, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            # Wait for success message to appear
            wait.until(EC.presence_of_element_located(self.SUCCESS_MESSAGE))
            return True
        except Exception:
            return False

    def wait_for_registration_page_to_load(self, timeout: int = 10) -> bool:
        """
        Wait for registration page to fully load

        Args:
            timeout: Timeout in seconds

        Returns:
            bool: True if page loaded successfully, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            # Wait for header to be visible
            wait.until(EC.presence_of_element_located(self.HEADER_TEXT))
            # Wait for submit button to be visible
            wait.until(EC.presence_of_element_located(self.SUBMIT_BUTTON))
            return True
        except Exception:
            return False

    def fill_registration_form(self, first_name: str, last_name: str, gender: str, 
                              date_of_birth: str, age: str, phone: str, village: str) -> bool:
        """
        Fill the entire registration form with provided data

        Args:
            first_name: First name
            last_name: Last name
            gender: Gender selection
            date_of_birth: Date of birth (DD/MM/YYYY)
            age: Age
            phone: Phone number
            village: Village selection

        Returns:
            bool: True if all fields filled successfully, False otherwise
        """
        try:
            print("   Filling registration form...")
            
            # Fill each field with logging
            print(f"   → Entering first name: {first_name}")
            self.enter_first_name(first_name)
            time.sleep(0.5)
            
            print(f"   → Entering last name: {last_name}")
            self.enter_last_name(last_name)
            time.sleep(0.5)
            
            print(f"   → Selecting gender: {gender}")
            self.select_gender(gender)
            time.sleep(0.5)
            
            print(f"   → Entering date of birth: {date_of_birth}")
            self.enter_date_of_birth(date_of_birth)
            time.sleep(0.5)
            
            print(f"   → Entering age: {age}")
            self.enter_age(age)
            time.sleep(0.5)
            
            print(f"   → Entering phone: {phone}")
            self.enter_phone_number(phone)
            time.sleep(0.5)
            
            print(f"   → Selecting village: {village}")
            self.select_village(village)
            time.sleep(0.5)
            
            print("   ✓ Form filled successfully")
            return True
            
        except Exception as e:
            print(f"   ✗ Error filling form: {e}")
            return False

    def get_form_data(self) -> dict:
        """
        Get all current form field values

        Returns:
            dict: Dictionary with all form field values
        """
        return {
            "first_name": self.get_first_name_value(),
            "last_name": self.get_last_name_value(),
            "gender": self.get_gender_value(),
            "age": self.get_age_value(),
            "phone": self.get_phone_value(),
        }
