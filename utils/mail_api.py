# File: utils/mail_api.py

import requests
import re
import time
from bs4 import BeautifulSoup

class MailTmApi:
    def __init__(self, email=None, password=None):
        self.base_url = "https://api.mail.tm"
        self.email = email
        self.password = password
        self.token = None
        self.headers = {}

    def create_account(self):
        resp = requests.get(f"{self.base_url}/domains")
        domain = resp.json()['hydra:member'][0]['domain']
        username = f"testuser{int(time.time())}"
        self.email = f"{username}@{domain}"
        self.password = "SuperSecurePassword123!"
        account_data = {"address": self.email, "password": self.password}
        requests.post(f"{self.base_url}/accounts", json=account_data)
        print(f"MailTM API: Account created -> {self.email}")
        return account_data

    def get_token(self):
        if not self.token:
            resp = requests.post(f"{self.base_url}/token", json={"address": self.email, "password": self.password})
            self.token = resp.json()['token']
            self.headers = {"Authorization": f"Bearer {self.token}"}
        return self.headers

    def wait_for_link(self, link_text_regex, timeout=120):
        deadline = time.time() + timeout
        headers = self.get_token()
        print("MailTM API: Waiting for new email...")
        while time.time() < deadline:
            try:
                resp = requests.get(f"{self.base_url}/messages", headers=headers)
                messages = resp.json()['hydra:member']
                if messages:
                    msg_id = messages[0]['id']
                    msg_resp = requests.get(f"{self.base_url}/messages/{msg_id}", headers=headers)
                    body_html = "".join(msg_resp.json().get('html', []))
                    soup = BeautifulSoup(body_html, 'html.parser')
                    link_tag = soup.find('a', string=re.compile(link_text_regex, re.I))
                    if link_tag and link_tag.get('href'):
                        print("MailTM API: ✅ Link found in email.")
                        return link_tag['href']
            except Exception as e:
                print(f"MailTM API: Error checking mail -> {e}")
            time.sleep(10)
        raise Exception("MailTM API: Did not receive email in time.")