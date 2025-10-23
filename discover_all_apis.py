# File: discover_all_apis.py

import json
from playwright.sync_api import sync_playwright, Request, Response
from faker import Faker

# Import all your Page Objects
from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage
from pages.password_reset_page import PasswordResetPage
from pages.profile_page import ProfilePage
from utils.mail_api import MailTmApi

BASE_URL = "https://front-end-qa.evendo.com"
CREDENTIALS_FILE = "credentials.json"
NEW_PASSWORD = "MyNewSecurePassword456!"
ULTRA_NEW_PASSWORD = "EvenMoreSecurePassword789!"

# --- Listener Functions ---

def handle_request(request: Request):
    """This function will be called for every request sent by the page."""
    if "/cms/" in request.url: # We are interested only in CMS API calls
        print("\n" + "="*40)
        print(f"➡️  REQUEST SENT:")
        print(f"   URL: {request.url}")
        print(f"   Method: {request.method}")
        
        # --- NEW: We are now capturing headers ---
        print("   --- Headers ---")
        for key, value in request.headers.items():
            # Print only the most important headers to avoid noise
            if key in ['content-type', 'referer', 'x-requested-with', 'user-agent']:
                 print(f"   {key}: {value}")
        
        if request.post_data:
            print("   --- Body ---")
            try:
                print(f"   {json.dumps(json.loads(request.post_data), indent=2)}")
            except json.JSONDecodeError:
                print(f"   {request.post_data}")
        print("="*40)

# The response handler can be simplified as we don't need it for this task
def handle_response(response: Response):
    pass


# --- Main Discovery Script ---
def discover_all_apis():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context(base_url=BASE_URL)
        page = context.new_page()

        page.on("request", handle_request)
        page.on("response", handle_response)
        
        mail_api = MailTmApi()

        print("\n🚀 STARTING REGISTRATION TO CAPTURE HEADERS 🚀")

        # --- We only need to run the registration part ---
        reg_credentials = mail_api.create_account()
        reg_page = RegistrationPage(page)
        reg_page.open()
        reg_page.submit_email(reg_credentials["address"])
        confirm_link = mail_api.wait_for_link(r'Click to verify', "Activate your Evendo Account")
        page.goto(confirm_link)
        reg_page.complete_registration("Test User", reg_credentials["password"])
        
        print("\n✅ API DISCOVERY FINISHED. Check the console for the headers of '/cms/confirm-user-verify'.")
        browser.close()

if __name__ == "__main__":
    discover_all_apis()