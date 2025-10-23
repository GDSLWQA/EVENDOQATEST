# File: api_tests/test_3_password_reset.py

import json
from utils.mail_api import MailTmApi
from api_tests.api_client import ApiClient

BASE_URL = "https://front-end-qa.evendo.com"
CREDENTIALS_FILE = "credentials.json"
NEW_PASSWORD = "MyNewSecurePassword456!"

def run_test():
    with open(CREDENTIALS_FILE, "r") as f:
        credentials = json.load(f)
    email = credentials["address"]
    
    mail_api = MailTmApi(email=email, password=credentials["password"])
    api_client = ApiClient(base_url=BASE_URL)
    
    # Step 1: Request password reset
    print("API Action: Requesting password reset...")
    api_client.post("/cms/forgot-password", data={"email": email, "score": 0.9})
    print("API Status: ✅ Reset request sent.")

    # Step 2: Get reset token from email
    reset_link = mail_api.wait_for_link(r'Click this link')
    reset_token = reset_link.split("token=")[1]
    
    # Step 3: Set new password with token
    print("API Action: Setting new password...")
    api_client.post("/cms/confirm-password-reset", data={
        "token": reset_token,
        "password": NEW_PASSWORD,
        "confirm_password": NEW_PASSWORD
    })
    print("API Status: ✅ Password has been reset.")

    # Step 4: Verify login with new password
    api_client.authenticate(email, NEW_PASSWORD)

    credentials["password"] = NEW_PASSWORD
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(credentials, f)
    print(f"Setup: New password saved to {CREDENTIALS_FILE}")

if __name__ == "__main__":
    run_test()