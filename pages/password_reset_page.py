from pages.base_page import BasePage

class PasswordResetPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.email_input = self.page.locator("#email")
        self.submit_button = self.page.locator("button[type='submit']")
        self.password_input = self.page.locator("#password")
        self.repassword_input = self.page.locator("#repassword")
        
    def open(self):
        print("Action: Opening password reset page...")
        self.page.goto("/forgot-password")

    def submit_email(self, email: str):
        print(f"Action: Submitting email for password reset -> {email}")
        self.email_input.fill(email)
        self.submit_button.click()
        
    def verify_request_submitted(self):
        self.page.wait_for_url("**/reset-confirm**")
        print("Status: ✅ Password reset request submitted.")

    def enter_new_password(self, password: str):
        print("Action: Entering new password...")
        self.password_input.fill(password)
        self.repassword_input.fill(password)
        self.submit_button.click()
        self.page.wait_for_url("**/login**")
        print("Status: ✅ Password successfully changed.")