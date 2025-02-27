#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import time
import urllib3

# Disable insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ANSI escape sequences for colors
RESET   = "\033[0m"
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
BLUE    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"

class RouterRebooter:
    def __init__(self, base_url="http://192.168.29.1/platform.cgi", 
                 username="admin", password="admin", debug=False):
        self.debug = debug
        self.base_url = base_url
        self.username = username
        self.password = password
        self.common_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "DNT": "1",
            "Origin": self.base_url,
            "Pragma": "no-cache",
            "Referer": self.base_url + "?page=factoryDefault.html",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/131.0.0.0 Safari/537.36")
        }
        self.session = requests.Session()

    def debug_print(self, message):
        if self.debug:
            print(f"{CYAN}[DEBUG] {message}{RESET}", end=" | ")

    def login(self):
        print(f"{CYAN}Log: Attempting login...{RESET}", end=" ")
        login_headers = self.common_headers.copy()
        login_headers["Cookie"] = "recordModified=1"
        login_data = {
            "thispage": "index.html",
            "users.username": self.username,
            "users.password": self.password,
            "button.login.users.dashboard": "Login"
        }
        self.debug_print(f"URL: {self.base_url} | Data: {login_data}")
        try:
            response = self.session.post(
                self.base_url,
                headers=login_headers,
                data=login_data,
                verify=False,
                timeout=10
            )
        except Exception as e:
            print(f"{RED}Failed: {e}{RESET}")
            return None

        self.debug_print(f"Status: {response.status_code}")
        if response.status_code != 200:
            print(f"{RED}Failed with code: {response.status_code}{RESET}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        token_input = soup.find("input", {"name": "token"})
        if token_input and token_input.has_attr("value"):
            token = token_input["value"]
            print(f"{GREEN}Success! Token: {token[:5]}...{RESET}")
            self.debug_print(f"Full Token: {token}")
            return token
        else:
            print(f"{RED}Token not found!{RESET}")
            return None

    def reboot(self):
        token = self.login()
        if not token:
            print(f"{RED}Aborted: No token.{RESET}")
            return

        print(f"{MAGENTA}Log: Initiating reboot in ", end="")
        for i in range(5, 0, -1):
            print(f"{YELLOW}{i}... ", end="", flush=True)
            time.sleep(1)
        print(f"{MAGENTA}Rebooting now!{RESET}")

        reboot_data = {
            "thispage": "factoryDefault.html",
            "token": token,
            "button.reboot.statusPage": "Reboot"
        }
        self.debug_print(f"Reboot Data: {reboot_data}")
        try:
            response = self.session.post(
                self.base_url,
                headers=self.common_headers,
                data=reboot_data,
                verify=False,
                timeout=10
            )
        except Exception as e:
            print(f"{RED}Reboot failed: {e}{RESET}")
            return

        self.debug_print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"{GREEN}Reboot initiated successfully!{RESET}")
        else:
            print(f"{RED}Reboot failed with code: {response.status_code}{RESET}")
            return

        self.wait_for_router()

    def wait_for_router(self, timeout=300):
        print(f"\r{CYAN}Log: Waiting for router to come back online...{RESET}", end=" ")
        time.sleep(20)  # Initial delay
        start_time = time.time()
        spinner = ['|', '/', '-', '\\']
        spin_index = 0

        while True:
            try:
                r = self.session.get(self.base_url, headers=self.common_headers, verify=False, timeout=5)
                if r.status_code == 200:
                    print(f"\r{GREEN}Router is back online!{RESET}")
                    self.debug_print(f"Response: {r.text[:50]}...")
                    break
            except Exception as e:
                self.debug_print(f"Check failed: {e}")

            elapsed = time.time() - start_time
            if elapsed > timeout:
                print(f"\r{RED}Timeout after {timeout}s!{RESET}")
                break

            print(f"\r{YELLOW}Status: {spinner[spin_index % len(spinner)]} ({int(elapsed)}s){RESET}", end='')
            spin_index += 1
            time.sleep(1)

    def run(self):
        print(f"{BLUE}JioReboot By Gaurav - Restarting your Jio router with style!{RESET}")
        self.reboot()

if __name__ == "__main__":
    rebooter = RouterRebooter(debug=True)  # Enable debug for testing
    rebooter.run()