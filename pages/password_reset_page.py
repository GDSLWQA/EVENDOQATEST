from pages.base_page import BasePage

class PasswordResetPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.email_input = self.page.locator("#email")
        self.submit_button = self.page.locator("button[type='submit']")
        self.password_input = self.page.locator("#password")
        self.repassword_input = self.page.locator("#repassword")
        
    def open(self):
        print("Открываем страницу сброса пароля...")
        self.page.goto("/forgot-password")

    def submit_email(self, email: str):
        print(f"Вводим email {email} для сброса пароля...")
        self.email_input.fill(email)
        self.submit_button.click()
        
    def verify_request_submitted(self):
        self.page.wait_for_url("**/reset-confirm**")
        print("✅ Запрос на сброс пароля отправлен.")

    def enter_new_password(self, password: str):
        print("Вводим новый пароль...")
        self.password_input.fill(password)
        self.repassword_input.fill(password)
        self.submit_button.click()
        self.page.wait_for_url("**/login**")
        print("✅ Пароль успешно изменен.")