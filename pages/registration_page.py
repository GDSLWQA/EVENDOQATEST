from pages.base_page import BasePage

class RegistrationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.email_input = self.page.locator("#email")
        self.submit_button = self.page.locator("button[type='submit']")
        self.name_input = self.page.locator("#name")
        self.password_input = self.page.locator("#password")
        self.repassword_input = self.page.locator("#repassword")
        
    def open(self):
        print("Открываем страницу регистрации...")
        self.page.goto("/registration")

    def submit_email(self, email: str):
        print(f"Вводим email {email} для регистрации...")
        self.email_input.fill(email)
        self.submit_button.click()
        
    def complete_registration(self, name: str, password: str):
        print("Завершаем регистрацию: вводим имя и пароль...")
        self.name_input.fill(name)
        self.password_input.fill(password)
        self.repassword_input.fill(password)
        self.submit_button.click()
        self.page.wait_for_url("**/login**")
        print("✅ Регистрация завершена.")