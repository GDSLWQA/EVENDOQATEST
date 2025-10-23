# File: api_tests/test_5_change_password.py

import json
from api_tests.api_client import ApiClient

BASE_URL = "https://front-end-qa.evendo.com"
CREDENTIALS_FILE = "credentials.json"
ULTRA_NEW_PASSWORD = "EvenMoreSecurePassword789!"

def run_test():
    api_client = ApiClient(base_url=BASE_URL)
    with open(CREDENTIALS_FILE, "r") as f:
        credentials = json.load(f)
    email = credentials["address"]
    current_password = credentials["password"]

    # Step 1: Authenticate with current password
    api_client.authenticate(email, current_password)

    # Step 2: Change password
    print("API Action: Changing password via API...")
    # NOTE: The endpoint '/cms/profile/change-password' is a guess.
    api_client.put("/cms/profile/change-password", data={
        "currentPassword": current_password,
        "newPassword": ULTRA_NEW_PASSWORD
    })
    print("API Status: ✅ Password change request sent.")

    # Step 3: Verify login with the ultra new password
    api_client.authenticate(email, ULTRA_NEW_PASSWORD)

    credentials["password"] = ULTRA_NEW_PASSWORD
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(credentials, f)
    print(f"Setup: Ultra new password saved to {CREDENTIALS_FILE}")

if __name__ == "__main__":
    run_test()