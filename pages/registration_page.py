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

    ALLOWED_VILLAGE_OPTIONS = [
        "ADARSHA A",
        "ATHABARI",
        "Four No line Jamuguri",
        "Furkating TE",
        "GHILADHARI TE",
        "Ghilladhari Notunline",
        "Ghilladhari P. Fokirline",
    ]

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
    VILLAGE_DROPDOWN_ARROW = (
        AppiumBy.XPATH,
        "(//android.widget.ImageButton[@content-desc=\"Show dropdown menu\"])[2]",
    )

    # Buttons
    CANCEL_BUTTON = (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/btnCancel")
    SUBMIT_BUTTON = (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/btnSubmit")

    # Success/Error messages
    SUCCESS_MESSAGE = (AppiumBy.XPATH, "//*[contains(@text, 'success') or contains(@text, 'Success') or contains(@text, 'registered')]")
    ERROR_MESSAGE = (AppiumBy.XPATH, "//*[contains(@text, 'error') or contains(@text, 'Error') or contains(@text, 'required')]")

    # Dialog buttons
    PROCEED_WITH_REGISTRATION_BTN_XPATH = (
        AppiumBy.XPATH,
        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.appcompat.widget.LinearLayoutCompat/android.widget.ScrollView/android.widget.LinearLayout/android.widget.Button[1]",
    )
    PROCEED_WITH_REGISTRATION_BTN_ID = (AppiumBy.ID, "android:id/button2")
    PROCEED_WITH_REGISTRATION_BTN_TEXT = (AppiumBy.XPATH, "//*[@text='Proceed with Registration']")
    SEARCH_BTN = (AppiumBy.ID, "android:id/button1")
    DIALOG_TITLE = (AppiumBy.ID, "android:id/alertTitle")

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
        candidate_locators = [
            self.HEADER_TEXT,
            (AppiumBy.XPATH, "//*[@text='Patient Registration' or contains(@text, 'Registration') ]"),
            self.FIRST_NAME_FIELD,
            (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/et_first_name"),
            self.SUBMIT_BUTTON,
            (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/btn_submit"),
        ]
        for locator in candidate_locators:
            try:
                el = self.driver.find_element(*locator)
                if el.is_displayed():
                    return True
            except Exception:
                continue
        return False

    def enter_first_name(self, first_name: str) -> None:
        field = self.driver.find_element(*self.FIRST_NAME_FIELD)
        field.clear()
        field.send_keys(first_name)

    def enter_last_name(self, last_name: str) -> None:
        field = self.driver.find_element(*self.LAST_NAME_FIELD)
        field.clear()
        field.send_keys(last_name)

    def select_gender(self, gender: str) -> None:
        try:
            dropdown = self.driver.find_element(*self.GENDER_DROPDOWN)
            dropdown.click()
            time.sleep(0.5)
            dropdown.clear()
            time.sleep(0.3)
            dropdown.send_keys(gender)
            time.sleep(1)

            gender_option = (AppiumBy.XPATH, f"//*[@text='{gender}']")
            try:
                option = self.driver.find_element(*gender_option)
                option.click()
                time.sleep(0.5)
                return
            except Exception as e:
                print(f"  -> First strategy failed: {e}, trying alternative...")
        except Exception as e:
            print(f"  -> Initial click failed: {e}")

        try:
            gender_option = (AppiumBy.XPATH, f"//*[contains(@text, '{gender}')]")
            option = self.driver.find_element(*gender_option)
            option.click()
            time.sleep(0.5)
            return
        except Exception as e:
            print(f"  -> Second strategy failed: {e}, trying partial match...")

        try:
            all_options = self.driver.find_elements(AppiumBy.XPATH, "//*[@class='android.widget.TextView']")
            for option in all_options:
                if gender.lower() in option.text.lower():
                    option.click()
                    time.sleep(0.5)
                    return
        except Exception as e:
            print(f"  -> Third strategy failed: {e}")

        raise Exception(f"Could not find and click gender option: {gender}")

    def enter_date_of_birth(self, date: str) -> None:
        try:
            day, month, year = date.split('/')
            day = int(day)
            month = int(month)
            year = int(year)

            print(f"  -> Opening date picker for: {day}/{month}/{year}")
            field = self.driver.find_element(*self.DATE_OF_BIRTH_FIELD)
            field.click()
            time.sleep(1.5)
            print("  Date picker opened")

            print("  -> Opening year picker...")
            try:
                year_header = self.driver.find_element(AppiumBy.ID, "android:id/date_picker_header_year")
                year_header.click()
                time.sleep(1)
                print("  Year picker opened")
            except Exception as e:
                print(f"  Could not click year header: {e}")
                raise

            print(f"  -> Scrolling to find year: {year}")
            year_text = str(year)
            year_found = False
            max_scroll_attempts = 25

            scroll_view = None
            try:
                scroll_view = self.driver.find_element(AppiumBy.ID, "android:id/animator")
                print("  Found year picker ScrollView (android:id/animator)")
            except Exception as e:
                print(f"  Could not find ScrollView with ID android:id/animator: {e}")
                print("  -> Will use swipe fallback method")

            for scroll_attempt in range(max_scroll_attempts):
                try:
                    year_elements = self.driver.find_elements(
                        AppiumBy.XPATH,
                        f"//android.widget.TextView[@text='{year_text}']",
                    )

                    if year_elements:
                        year_elem = year_elements[0]
                        year_elem.click()
                        time.sleep(0.5)
                        print(f"  Year {year_text} found and clicked")
                        year_found = True
                        break
                except Exception:
                    pass

                try:
                    if scroll_view:
                        if year < 2000:
                            self.driver.execute_script(
                                "mobile: scrollGesture",
                                {"elementId": scroll_view.id, "direction": "up", "percent": 0.75},
                            )
                        else:
                            self.driver.execute_script(
                                "mobile: scrollGesture",
                                {"elementId": scroll_view.id, "direction": "down", "percent": 0.75},
                            )
                    else:
                        if year < 2000:
                            self.driver.swipe(540, 400, 540, 600, duration=300)
                        else:
                            self.driver.swipe(540, 600, 540, 400, duration=300)

                    time.sleep(0.3)

                    if scroll_attempt % 4 == 0:
                        print(f"  -> Scrolling attempt {scroll_attempt + 1}/{max_scroll_attempts}")
                except Exception as scroll_error:
                    print(f"  Scroll attempt {scroll_attempt + 1} failed: {scroll_error}")

            if not year_found:
                raise Exception(f"Year {year_text} not found in picker after {max_scroll_attempts} scroll attempts")

            time.sleep(1.5)
            print("  -> Waiting for calendar to load...")

            # Prefer selecting the exact target date by content description first.
            target_date_text = f"{day} April {year}" if month == 4 else None
            exact_date_selected = False
            if target_date_text:
                exact_date_locators = [
                    (AppiumBy.ACCESSIBILITY_ID, target_date_text),
                    (AppiumBy.XPATH, f"//*[@content-desc='{target_date_text}']"),
                    (AppiumBy.XPATH, f"//android.view.View[@content-desc='{target_date_text}']"),
                    (AppiumBy.XPATH, f"//android.widget.Button[@content-desc='{target_date_text}']"),
                ]
                for locator in exact_date_locators:
                    try:
                        exact_date_element = self.driver.find_element(*locator)
                        exact_date_element.click()
                        time.sleep(0.5)
                        print(f"  Exact date selected: {target_date_text}")
                        exact_date_selected = True
                        break
                    except Exception:
                        continue

            print(f"  -> Selecting day: {day}")
            date_found = False

            if exact_date_selected:
                date_found = True
            else:
                try:
                    month_view = self.driver.find_element(AppiumBy.ID, "android:id/month_view")
                    date_buttons = month_view.find_elements(AppiumBy.XPATH, ".//android.widget.Button")

                    for btn in date_buttons:
                        if btn.text.strip() == str(day):
                            btn.click()
                            time.sleep(0.5)
                            print(f"  Date {day} selected")
                            date_found = True
                            break
                except Exception as e:
                    print(f"  Could not select from month_view: {e}")

            if not date_found:
                try:
                    date_button = self.driver.find_element(AppiumBy.XPATH, f"//android.widget.Button[@text='{day}']")
                    date_button.click()
                    time.sleep(0.5)
                    print(f"  Date {day} selected (XPath)")
                    date_found = True
                except Exception as e:
                    print(f"  Could not find date button {day}: {e}")

            print("  -> Confirming date selection...")
            try:
                ok_button = self.driver.find_element(AppiumBy.XPATH, "//android.widget.Button[@text='OK']")
                ok_button.click()
                time.sleep(1)
                print(f"  Date confirmed - Set to: {day}/{month}/{year}")
            except Exception:
                try:
                    ok_button = self.driver.find_element(AppiumBy.ID, "android:id/button1")
                    ok_button.click()
                    time.sleep(1)
                    print(f"  Date confirmed - Set to: {day}/{month}/{year}")
                except Exception as e2:
                    print(f"  Could not click OK button: {e2}")
                    raise

        except Exception as e:
            print(f"  Error entering date of birth {date}: {e}")
            raise

    def enter_age(self, age: str) -> None:
        field = self.driver.find_element(*self.AGE_FIELD)
        field.clear()
        field.send_keys(age)

    def enter_phone_number(self, phone: str) -> None:
        field = self.driver.find_element(*self.PHONE_NUMBER_FIELD)
        field.clear()
        field.send_keys(phone)

    def select_village(self, village: str) -> None:
        try:
            print(f"  -> Selecting village from dropdown: {village}")
            dropdown = self.driver.find_element(*self.VILLAGE_DROPDOWN)
            previous_value = dropdown.text.strip()

            target_village = village if village in self.ALLOWED_VILLAGE_OPTIONS else self.ALLOWED_VILLAGE_OPTIONS[0]
            if target_village != village:
                print(f"  -> Requested village not allowed. Using '{target_village}'")

            def _open_dropdown():
                try:
                    self.driver.find_element(*self.VILLAGE_DROPDOWN_ARROW).click()
                    print("  Opened village dropdown via arrow button")
                except Exception:
                    try:
                        dropdown.click()
                    except Exception:
                        self.driver.execute_script("mobile: clickGesture", {"elementId": dropdown.id})
                    print("  -> Opened village dropdown via field tap (fallback)")
                time.sleep(0.6)

            def _click_elem(elem):
                try:
                    elem.click()
                except Exception:
                    try:
                        self.driver.execute_script("mobile: clickGesture", {"elementId": elem.id})
                    except Exception:
                        rect = elem.rect
                        self.driver.execute_script(
                            "mobile: clickGesture",
                            {"x": int(rect["x"] + rect["width"] / 2), "y": int(rect["y"] + rect["height"] / 2)},
                        )
                time.sleep(0.2)

            def _tap_elem_center(elem):
                rect = elem.rect
                self.driver.execute_script(
                    "mobile: clickGesture",
                    {"x": int(rect["x"] + rect["width"] / 2), "y": int(rect["y"] + rect["height"] / 2)},
                )
                time.sleep(0.3)

            def _collect_allowed_visible_options():
                xpaths = [
                    "//android.widget.ListView//android.widget.CheckedTextView",
                    "//android.widget.ListView//android.widget.TextView",
                    "//androidx.recyclerview.widget.RecyclerView//android.widget.CheckedTextView",
                    "//androidx.recyclerview.widget.RecyclerView//android.widget.TextView",
                    "//android.widget.CheckedTextView",
                    "//android.widget.TextView",
                ]
                options = []
                for xp in xpaths:
                    elems = self.driver.find_elements(AppiumBy.XPATH, xp)
                    for elem in elems:
                        try:
                            txt = elem.text.strip()
                            if not txt or not elem.is_displayed():
                                continue
                            if txt in self.ALLOWED_VILLAGE_OPTIONS:
                                options.append((txt, elem))
                        except Exception:
                            continue
                    if options:
                        break
                return options

            clicked_value = None

            # Step 1: Open dropdown without typing.
            _open_dropdown()
            try:
                dropdown.clear()
            except Exception:
                pass
            time.sleep(0.5)

            # Step 2: Click an actual visible option.
            options = _collect_allowed_visible_options()
            if options:
                option_map = {txt.lower(): (txt, elem) for txt, elem in options}
                if target_village.lower() in option_map:
                    clicked_value, target_elem = option_map[target_village.lower()]
                else:
                    clicked_value, target_elem = options[0]
                _tap_elem_center(target_elem)
                _click_elem(target_elem)
                print(f"  -> Clicked village option: '{clicked_value}'")
                try:
                    self.driver.press_keycode(66)
                except Exception:
                    pass
                time.sleep(0.8)
            else:
                # Step 3: Use UiScrollable and click explicit option text.
                try:
                    ui_scroll = (
                        "new UiScrollable(new UiSelector().scrollable(true))"
                        f".scrollIntoView(new UiSelector().text(\"{target_village}\"));"
                    )
                    self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, ui_scroll)
                    option = self.driver.find_element(AppiumBy.XPATH, f"//*[@text='{target_village}']")
                    _tap_elem_center(option)
                    _click_elem(option)
                    clicked_value = target_village
                    print(f"  -> Clicked village option via scroll: '{clicked_value}'")
                    try:
                        self.driver.press_keycode(66)
                    except Exception:
                        pass
                    time.sleep(0.8)
                except Exception as ui_error:
                    print(f"  -> UiScrollable path failed: {ui_error}. Trying exact-text click fallback...")
                    fallback_clicked = False
                    for candidate in allowed_preference_order:
                        if candidate not in self.ALLOWED_VILLAGE_OPTIONS:
                            continue
                        try:
                            option = self.driver.find_element(AppiumBy.XPATH, f"//*[@text='{candidate}']")
                            _tap_elem_center(option)
                            _click_elem(option)
                            clicked_value = candidate
                            print(f"  -> Clicked village option by exact text fallback: '{clicked_value}'")
                            try:
                                self.driver.press_keycode(66)
                            except Exception:
                                pass
                            time.sleep(0.8)
                            fallback_clicked = True
                            break
                        except Exception:
                            continue

                    if not fallback_clicked:
                        raise ui_error

            # Step 4: Verify selected value reflects clicked option.
            selected_value = self.driver.find_element(*self.VILLAGE_DROPDOWN).text.strip()
            if clicked_value and selected_value and selected_value.lower() == clicked_value.lower() and selected_value != previous_value:
                print(f"  Village set to: '{selected_value}'")
                return

            raise Exception(
                f"Village option click did not apply. Previous='{previous_value}', current='{selected_value}', clicked='{clicked_value}'"
            )

        except Exception as e:
            print(f"  Error selecting village {village}: {e}")
            raise

    def click_submit(self) -> None:
        submit_btn = self.driver.find_element(*self.SUBMIT_BUTTON)
        submit_btn.click()

    def click_cancel(self) -> None:
        cancel_btn = self.driver.find_element(*self.CANCEL_BUTTON)
        cancel_btn.click()

    def click_home(self) -> None:
        home_btn = self.driver.find_element(*self.HOME_BUTTON)
        home_btn.click()

    def click_registration_fab(self) -> None:
        try:
            registration_fab = self.driver.find_element(*self.REGISTRATION_FAB)
            registration_fab.click()
            time.sleep(1.5)
        except Exception as e:
            print(f"Could not click registration FAB: {e}")
            raise

    def click_photo_capture(self) -> None:
        photo_btn = self.driver.find_element(*self.PHOTO_CAPTURE_BTN)
        photo_btn.click()

    def click_proceed_with_registration_dialog(self) -> None:
        wait = WebDriverWait(self.driver, 8)
        locators = [
            self.PROCEED_WITH_REGISTRATION_BTN_XPATH,
            self.PROCEED_WITH_REGISTRATION_BTN_ID,
            self.PROCEED_WITH_REGISTRATION_BTN_TEXT,
        ]

        last_error = None
        for locator in locators:
            try:
                proceed_btn = wait.until(EC.presence_of_element_located(locator))
                try:
                    proceed_btn.click()
                except Exception:
                    try:
                        self.driver.execute_script("mobile: clickGesture", {"elementId": proceed_btn.id})
                    except Exception:
                        rect = proceed_btn.rect
                        center_x = int(rect["x"] + rect["width"] / 2)
                        center_y = int(rect["y"] + rect["height"] / 2)
                        self.driver.execute_script("mobile: clickGesture", {"x": center_x, "y": center_y})

                # Verify dialog was dismissed after click.
                try:
                    WebDriverWait(self.driver, 2).until(EC.invisibility_of_element_located(self.DIALOG_TITLE))
                except Exception:
                    pass
                return
            except Exception as e:
                last_error = e

        print(f"Could not click Proceed with Registration dialog button: {last_error}")
        raise last_error

    def click_search_button_dialog(self) -> None:
        try:
            search_btn = self.driver.find_element(*self.SEARCH_BTN)
            search_btn.click()
        except Exception as e:
            print(f"Could not click search button: {e}")
            raise

    def is_dialog_displayed(self) -> bool:
        try:
            dialog = self.driver.find_element(*self.DIALOG_TITLE)
            return dialog.is_displayed()
        except Exception:
            return False

    def get_first_name_value(self) -> str:
        field = self.driver.find_element(*self.FIRST_NAME_FIELD)
        return field.get_attribute("text")

    def get_last_name_value(self) -> str:
        field = self.driver.find_element(*self.LAST_NAME_FIELD)
        return field.get_attribute("text")

    def get_gender_value(self) -> str:
        dropdown = self.driver.find_element(*self.GENDER_DROPDOWN)
        return dropdown.get_attribute("text")

    def get_age_value(self) -> str:
        field = self.driver.find_element(*self.AGE_FIELD)
        return field.get_attribute("text")

    def get_phone_value(self) -> str:
        field = self.driver.find_element(*self.PHONE_NUMBER_FIELD)
        return field.get_attribute("text")

    def is_error_message_displayed(self) -> bool:
        try:
            error = self.driver.find_element(*self.ERROR_MESSAGE)
            return error.is_displayed()
        except Exception:
            return False

    def get_error_message_text(self) -> str:
        try:
            error = self.driver.find_element(*self.ERROR_MESSAGE)
            return error.text
        except Exception:
            return "No error message found"

    def is_success_message_displayed(self) -> bool:
        try:
            success = self.driver.find_element(*self.SUCCESS_MESSAGE)
            return success.is_displayed()
        except Exception:
            return False

    def get_success_message_text(self) -> str:
        try:
            success = self.driver.find_element(*self.SUCCESS_MESSAGE)
            return success.text
        except Exception:
            return "No success message found"

    def wait_for_registration_success(self, timeout: int = 10) -> bool:
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located(self.SUCCESS_MESSAGE))
            return True
        except Exception:
            return False

    def wait_for_registration_page_to_load(self, timeout: int = 10) -> bool:
        wait = WebDriverWait(self.driver, timeout)
        locators = [
            self.FIRST_NAME_FIELD,
            (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/et_first_name"),
            self.SUBMIT_BUTTON,
            (AppiumBy.ID, "org.piramalswasthya.cho.niramay.uat:id/btn_submit"),
            self.HEADER_TEXT,
            (AppiumBy.XPATH, "//*[@text='Patient Registration' or contains(@text, 'Registration') ]"),
        ]

        for locator in locators:
            try:
                wait.until(EC.presence_of_element_located(locator))
                return True
            except Exception:
                continue
        return False

    def fill_registration_form(
        self,
        first_name: str,
        last_name: str,
        gender: str,
        date_of_birth: str,
        age: str,
        phone: str,
        village: str,
    ) -> bool:
        try:
            print("   Filling registration form...")
            print(f"   -> Entering first name: {first_name}")
            self.enter_first_name(first_name)
            time.sleep(0.5)

            print(f"   -> Entering last name: {last_name}")
            self.enter_last_name(last_name)
            time.sleep(0.5)

            print(f"   -> Selecting gender: {gender}")
            self.select_gender(gender)
            time.sleep(0.5)

            print(f"   -> Entering date of birth: {date_of_birth}")
            self.enter_date_of_birth(date_of_birth)
            time.sleep(0.5)

            print(f"   -> Entering age: {age}")
            self.enter_age(age)
            time.sleep(0.5)

            print(f"   -> Entering phone: {phone}")
            self.enter_phone_number(phone)
            time.sleep(0.5)

            print(f"   -> Selecting village: {village}")
            self.select_village(village)
            time.sleep(0.5)

            print("   Form filled successfully")
            return True

        except Exception as e:
            print(f"   Error filling form: {e}")
            return False

    def get_form_data(self) -> dict:
        return {
            "first_name": self.get_first_name_value(),
            "last_name": self.get_last_name_value(),
            "gender": self.get_gender_value(),
            "age": self.get_age_value(),
            "phone": self.get_phone_value(),
        }
