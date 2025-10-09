import json
from playwright.sync_api import sync_playwright
from utils.mail_api import MailTmApi
from pages.registration_page import RegistrationPage

BASE_URL = "https://front-end-qa.evendo.com"
CREDENTIALS_FILE = "credentials.json"

def run_test():
    mail_api = MailTmApi()
    credentials = mail_api.create_account()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context(base_url=BASE_URL)
        page = context.new_page()
        
        reg_page = RegistrationPage(page)
        reg_page.open()
        reg_page.submit_email(credentials["address"])
        
        confirm_link = mail_api.wait_for_link(r'Click to verify')
        page.goto(confirm_link)
        
        reg_page.complete_registration("Test User", credentials["password"])
        
        with open(CREDENTIALS_FILE, "w") as f:
            json.dump(credentials, f)
        print(f"Setup: Credentials saved to {CREDENTIALS_FILE}")
        
        browser.close()

if __name__ == "__main__":
    run_test()