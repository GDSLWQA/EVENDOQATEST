# File: tests/test_4_fill_profile.py

import json
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from faker import Faker

BASE_URL = "https://front-end-qa.evendo.com"
CREDENTIALS_FILE = "credentials.json"

def run_test():
    # --- 1. Prepare Data ---
    fake = Faker()
    profile_data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "address": fake.street_address(),
        "zip_code": fake.zipcode(),
        "city": fake.city(),
        "country": "United States",
        "phone_number": fake.msisdn()[2:]
    }
    
    with open(CREDENTIALS_FILE, "r") as f:
        credentials = json.load(f)
    email = credentials["address"]
    new_password = credentials["password"]

    # --- 2. Execute Test ---
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context(base_url=BASE_URL)
        page = context.new_page()

        login_page = LoginPage(page)
        profile_page = ProfilePage(page)
        
        # --- 3. Log In ---
        login_page.open()
        login_page.login(email, new_password)
        login_page.verify_login_successful()
        
        # --- 4. Fill and Save Profile ---
        profile_page.fill_profile_form(**profile_data)
        profile_page.save_changes()
        
        # --- 5. Re-login to Verify ---
       
        print("Action: Manually navigating to login page to re-login and verify.")
        login_page.open()
        login_page.login(email, new_password)
        login_page.verify_login_successful()

        # --- 6. Verify Data Was Saved ---
        current_data = profile_page.get_form_data()
        
        print("Action: Verifying saved data...")
        assert profile_data["first_name"] == current_data["first_name"]
        assert profile_data["last_name"] == current_data["last_name"]
        assert profile_data["address"] == current_data["address"]
        assert profile_data["zip_code"] == current_data["zip_code"]
        assert profile_data["city"] == current_data["city"]
        assert profile_data["phone_number"] in current_data["phone_number"]
        
        print("Status: ✅ All profile data verified successfully!")

        browser.close()

if __name__ == "__main__":
    run_test()