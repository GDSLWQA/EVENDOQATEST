# File: pages/login_page.py

from pages.base_page import BasePage
from playwright.sync_api import expect

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.email_input = self.page.locator("#email")
        self.password_input = self.page.locator("#password")
        self.submit_button = self.page.locator("button[type='submit']")

    def open(self):
        print("Action: Opening login page...")
        self.page.goto("/login")
        
    def login(self, email: str, password: str):
        print(f"Action: Logging in as -> {email}")
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()
        
    def verify_login_successful(self):
        self.page.wait_for_url("**/profile**")
        
       
        save_button = self.page.get_by_role("button", name="Save Changes")
        expect(save_button).to_be_visible(timeout=10000)
        
        print("Status: ✅ Login successful, profile page is loaded.")