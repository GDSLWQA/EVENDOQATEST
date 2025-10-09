import json
from playwright.sync_api import sync_playwright
from utils.mail_api import MailTmApi
from pages.password_reset_page import PasswordResetPage
from pages.login_page import LoginPage

BASE_URL = "https://front-end-qa.evendo.com"
CREDENTIALS_FILE = "credentials.json"
NEW_PASSWORD = "MyNewSecurePassword456!"

def run_test():
    with open(CREDENTIALS_FILE, "r") as f:
        credentials = json.load(f)
    email = credentials["address"]
    password = credentials["password"]

    mail_api = MailTmApi(email=email, password=password)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context(base_url=BASE_URL)
        page = context.new_page()

        reset_page = PasswordResetPage(page)
        reset_page.open()
        reset_page.submit_email(email)
        reset_page.verify_request_submitted()

        reset_link = mail_api.wait_for_link(r'Click this link to reset your password')
        page.goto(reset_link)
        reset_page.enter_new_password(NEW_PASSWORD)

        login_page = LoginPage(page)
        login_page.login(email, NEW_PASSWORD)
        login_page.verify_login_successful()
        
        credentials["password"] = NEW_PASSWORD
        with open(CREDENTIALS_FILE, "w") as f:
            json.dump(credentials, f)
        print(f"Setup: New password saved to {CREDENTIALS_FILE}")

        browser.close()

if __name__ == "__main__":
    run_test()