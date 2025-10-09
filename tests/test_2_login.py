import json
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage

BASE_URL = "https://front-end-qa.evendo.com"
CREDENTIALS_FILE = "credentials.json"

def run_test():
    with open(CREDENTIALS_FILE, "r") as f:
        credentials = json.load(f)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context(base_url=BASE_URL)
        page = context.new_page()

        login_page = LoginPage(page)
        login_page.open()
        login_page.login(credentials["address"], credentials["password"])
        login_page.verify_login_successful()
        
        browser.close()

if __name__ == "__main__":
    run_test()