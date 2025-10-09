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
        user_name_element = self.page.get_by_role("link", name="Test User")
        expect(user_name_element).to_be_visible(timeout=10000)
        print("Status: ✅ Login successful, user name is visible.")