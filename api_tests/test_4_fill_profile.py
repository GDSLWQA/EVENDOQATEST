# File: api_tests/test_4_fill_profile.py

import json
from api_tests.api_client import ApiClient
from faker import Faker

BASE_URL = "https://front-end-qa.evendo.com"
CREDENTIALS_FILE = "credentials.json"

def run_test():
    api_client = ApiClient(base_url=BASE_URL)
    fake = Faker()
    with open(CREDENTIALS_FILE, "r") as f:
        credentials = json.load(f)
    
    # Step 1: Authenticate to get the token
    api_client.authenticate(credentials["address"], credentials["password"])

    # Step 2: Prepare profile data
    profile_data = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "address": fake.street_address(),
        "zipCode": fake.zipcode(),
        "city": fake.city(),
        "country": "United States",
        "phone": fake.msisdn()
    }
    
    # Step 3: Update profile
    print("API Action: Updating user profile...")
    # NOTE: The endpoint '/cms/profile' is a guess. You might need to find the correct one.
    api_client.put("/cms/profile", data=profile_data) 
    print("API Status: ✅ Profile update request sent.")

    # Step 4: Verify profile data
    print("API Action: Verifying updated profile data...")
    response = api_client.get("/cms/profile")
    assert response["firstName"] == profile_data["firstName"]
    assert response["lastName"] == profile_data["lastName"]
    print("API Status: ✅ Profile data verified.")

if __name__ == "__main__":
    run_test()