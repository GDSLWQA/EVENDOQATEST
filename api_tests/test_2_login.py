# File: api_tests/test_2_login.py

import json
from api_tests.api_client import ApiClient

BASE_URL = "https://front-end-qa.evendo.com"
CREDENTIALS_FILE = "credentials.json"

def run_test():
    api_client = ApiClient(base_url=BASE_URL)
    with open(CREDENTIALS_FILE, "r") as f:
        credentials = json.load(f)

    # Authenticate and implicitly check that it doesn't fail
    api_client.authenticate(credentials["address"], credentials["password"])
    
if __name__ == "__main__":
    run_test()