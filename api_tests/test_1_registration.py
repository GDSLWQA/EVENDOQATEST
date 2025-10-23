# File: api_tests/test_1_registration.py

import json
from playwright.sync_api import sync_playwright # We will use Playwright's power
from utils.mail_api import MailTmApi
# We no longer need ApiClient for this specific test

BASE_URL = "https://front-end-qa.evendo.com"
CREDENTIALS_FILE = "credentials.json"

def run_test():
    mail_api = MailTmApi()
    
    # Step 1: Create email account
    credentials = mail_api.create_account()
    email = credentials["address"]
    password = credentials["password"]
    
    # We will use a real browser to establish the necessary session context
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) # Runs in the background
        page = browser.new_page()

        # Step 2: Initial registration request (using the browser's context)
        print("API Action: Sending initial registration request...")
        api_request_context = page.request
        api_request_context.post(f"{BASE_URL}/cms/create-user", data={"email": email, "score": 0.9, "condition1": False, "condition2": False})
        print("API Status: ✅ Initial request sent.")

        # Step 3: Get the tracking link and visit it with the browser
        tracking_link = mail_api.wait_for_link(r'Click to verify', "Activate your Evendo Account")
        
        # --- FINAL FIX ---
        # By visiting the link with the page object, we ensure all cookies and session data are correctly set.
        print("API Action: Visiting confirmation link to establish session...")
        page.goto(tracking_link)
        final_url = page.url
        print(f"API Status: ✅ Session established. Final URL is: {final_url}")
        
        confirm_token = final_url.split("token=")[1]
        
        # Step 4: Finalize registration using the browser's authenticated API context
        headers = {'Referer': final_url}
        
        print("API Action: Finalizing registration with full browser context...")
        response = api_request_context.post(
            f"{BASE_URL}/cms/confirm-user-verify", 
            data={
                "firstName": "Test User",
                "token": confirm_token,
                "password": password,
                "confirm_password": password
            },
            headers=headers
        )
        
        assert response.ok, f"Final registration failed with status {response.status}"
        print("API Status: ✅ Registration complete.")

        browser.close()

    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(credentials, f)
    print(f"Setup: Credentials saved to {CREDENTIALS_FILE}")

if __name__ == "__main__":
    run_test()