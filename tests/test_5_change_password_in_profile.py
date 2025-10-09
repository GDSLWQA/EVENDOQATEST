# File: tests/test_5_change_password_in_profile.py

import json
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage

BASE_URL = "https://front-end-qa.evendo.com"
CREDENTIALS_FILE = "credentials.json"
ULTRA_NEW_PASSWORD = "EvenMoreSecurePassword789!"

def run_test():
    with open(CREDENTIALS_FILE, "r") as f:
        credentials = json.load(f)
    email = credentials["address"]
    current_password = credentials["password"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context(base_url=BASE_URL)
        page = context.new_page()

        login_page = LoginPage(page)
        profile_page = ProfilePage(page)
        
        # --- 1. Log in with the current password ---
        login_page.open()
        login_page.login(email, current_password)
        login_page.verify_login_successful()
        
        # --- 2. Navigate to the change password page and change it ---
        profile_page.navigate_to_change_password()
        profile_page.update_password(current_password, ULTRA_NEW_PASSWORD)
        
        # --- 3. Verify login with the newest password ---
        # --- FINAL FIX ---
        # After the page reloads, we are logged out.
        # We now manually open the login page to verify.
        print("Action: Manually opening login page to verify new password...")
        login_page.open() 
        login_page.login(email, ULTRA_NEW_PASSWORD)
        login_page.verify_login_successful()

        # Update the credentials file for any future tests
        credentials["password"] = ULTRA_NEW_PASSWORD
        with open(CREDENTIALS_FILE, "w") as f:
            json.dump(credentials, f)
        print(f"Setup: Ultra new password saved to {CREDENTIALS_FILE}")

        browser.close()

if __name__ == "__main__":
    run_test()