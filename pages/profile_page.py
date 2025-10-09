# File: pages/profile_page.py

from pages.base_page import BasePage
from playwright.sync_api import expect

class ProfilePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.first_name_input = self.page.locator("#first_name")
        self.last_name_input = self.page.locator("#last_name")
        self.address_input = self.page.locator("#address")
        self.zip_code_input = self.page.locator("#zip_code")
        self.city_input = self.page.locator("#city")
        self.country_dropdown = self.page.locator("#country .niceCountryInputMenu")
        self.phone_country_dropdown = self.page.locator("#profileUpdate > div:nth-child(5) > div > div > div")
        self.phone_number_input = self.page.locator("#phone_number")
        self.save_button = self.page.get_by_role("button", name="Save Changes")

    def fill_profile_form(self, first_name, last_name, address, zip_code, city, country, phone_number):
        """Fills all fields in the profile form, including phone."""
        print("Action: Filling out profile information...")
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.address_input.fill(address)
        self.zip_code_input.fill(zip_code)
        self.city_input.fill(city)
        self.country_dropdown.click()
        self.page.locator(f"div.niceCountryInputMenuDropdownContent >> text={country}").first.click()
        self.phone_country_dropdown.click()
        self.page.locator(f"li.iti__country.iti__standard[data-country-code='us']").click()
        self.phone_number_input.fill(phone_number)
        print("Status: ✅ Profile form filled.")

    def save_changes(self):
        """Just clicks the save button."""
        print("Action: Clicking 'Save Changes'...")
        self.save_button.click()
       
        self.page.wait_for_timeout(1000)
        print("Status: ✅ Save button clicked.")

    def get_form_data(self):
        """Gets the current values from the form fields for verification."""
        print("Action: Getting current data from profile form...")
        return {
            "first_name": self.first_name_input.input_value(),
            "last_name": self.last_name_input.input_value(),
            "address": self.address_input.input_value(),
            "zip_code": self.zip_code_input.input_value(),
            "city": self.city_input.input_value(),
            "phone_number": self.phone_number_input.input_value(),
        }