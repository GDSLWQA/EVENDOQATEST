# File: api_tests/api_client.py

import requests

class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session() # This session object will store cookies automatically
        self.token = None

    def post(self, endpoint, data, headers=None):
        """Sends a POST request using the session."""
        url = self.base_url + endpoint
        response = self.session.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json() if response.content else {}

    def put(self, endpoint, data):
        """Sends a PUT request with authorization."""
        if not self.token:
            raise Exception("Authentication token is not set. Please log in first.")
        
        url = self.base_url + endpoint
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.session.put(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json() if response.content else {}
    
    def get(self, endpoint):
        """Sends a GET request with authorization."""
        if not self.token:
            raise Exception("Authentication token is not set. Please log in first.")
            
        url = self.base_url + endpoint
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        return response.json() if response.content else {}

    def follow_redirect_and_get_url(self, url):
        """
        --- NEW METHOD ---
        Uses the shared session to visit a URL, which captures any cookies set during the process.
        """
        print(f"API Action: Following redirect link -> {url}")
        response = self.session.get(url, allow_redirects=True)
        response.raise_for_status()
        final_url = response.url
        print(f"API Status: ✅ Final URL is: {final_url}")
        return final_url

    def authenticate(self, email, password):
        """Logs in and saves the auth token."""
        print("API Action: Authenticating...")
        response = self.post("/cms/authenticate", data={"email": email, "password": password})
        self.token = response.get("token")
        assert self.token, "Failed to get auth token from login response."
        print("API Status: ✅ Authentication successful, token stored.")
        return self.token