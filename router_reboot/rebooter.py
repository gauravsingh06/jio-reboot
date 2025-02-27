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
                 username="admin", password="Helloji@12", debug=False):
        # Debug flag: when True, additional internal data is printed.
        self.debug = debug

        # Router configuration variables
        self.base_url = base_url
        self.username = username
        self.password = password

        # Common headers for both requests
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
        # Create a session to persist cookies between requests.
        self.session = requests.Session()

    def debug_print(self, message):
        """Print debug messages only if debug mode is enabled."""
        if self.debug:
            print(f"{CYAN}[DEBUG]{RESET} {message}")

    def login(self):
        """Performs the login to the router and returns the token extracted from the response."""
        print(f"{CYAN}Attempting to log in to the router...{RESET}")
        login_headers = self.common_headers.copy()
        # Set initial cookie as per the first cURL request.
        login_headers["Cookie"] = "recordModified=1"

        login_data = {
            "thispage": "index.html",
            "users.username": self.username,
            "users.password": self.password,
            "button.login.users.dashboard": "Login"
        }
        self.debug_print(f"Login URL: {self.base_url}")
        self.debug_print(f"Login headers: {login_headers}")
        self.debug_print(f"Login data: {login_data}")

        try:
            response = self.session.post(
                self.base_url,
                headers=login_headers,
                data=login_data,
                verify=False,
                timeout=10
            )
        except Exception as e:
            print(f"{RED}Login request failed: {e}{RESET}")
            return None

        self.debug_print(f"Login response status code: {response.status_code}")
        self.debug_print(f"Login response content: {response.text[:200]}...")  # Print only first 200 chars

        if response.status_code != 200:
            print(f"{RED}Login failed with status code: {response.status_code}{RESET}")
            return None

        # Parse the HTML to extract the token from an <input name="token" ...>
        soup = BeautifulSoup(response.text, "html.parser")
        token_input = soup.find("input", {"name": "token"})

        if token_input and token_input.has_attr("value"):
            token = token_input["value"]
            print(f"{GREEN}Logged in successfully!{RESET}")
            self.debug_print(f"Token acquired: {token}")
            return token
        else:
            print(f"{RED}Token not found in login response!{RESET}")
            return None

    def reboot(self):
        """Logs in to obtain the token, then sends the reboot request."""
        token = self.login()
        if not token:
            print(f"{RED}Reboot aborted: Unable to retrieve token.{RESET}")
            return

        # Add a humorous countdown before initiating the reboot
        countdown_seconds = 5
        print(f"\n{MAGENTA}Get ready for the ultimate router reboot extravaganza!")
        for i in range(countdown_seconds, 0, -1):
            print(f"{YELLOW}Rebooting in {i}... Brace yourself!{RESET}")
            time.sleep(1)
        print(f"{MAGENTA}3... 2... 1... BOOM!{RESET}\n")

        reboot_data = {
            "thispage": "factoryDefault.html",
            "token": token,
            "button.reboot.statusPage": "Reboot"
        }
        self.debug_print(f"Reboot data: {reboot_data}")

        try:
            response = self.session.post(
                self.base_url,
                headers=self.common_headers,
                data=reboot_data,
                verify=False,
                timeout=10
            )
        except Exception as e:
            print(f"{RED}Reboot request failed: {e}{RESET}")
            return

        self.debug_print(f"Reboot response status code: {response.status_code}")
        self.debug_print(f"Reboot response content: {response.text[:200]}...")

        if response.status_code == 200:
            print(f"{GREEN}Router reboot successfully initiated! Now, let the magic happen...{RESET}")
        else:
            print(f"{RED}Reboot failed with status code: {response.status_code}{RESET}")
            return

        self.wait_for_router()

    def wait_for_router(self, timeout=300):
        """Keep checking if the router is up and display a spinner while waiting."""
        print(f"\n{CYAN}Waiting for the router to wake up from its beauty sleep...{RESET}")
        time.sleep(20)  # Initial delay before checking
        start_time = time.time()
        spinner = ['|', '/', '-', '\\']
        spin_index = 0

        while True:
            try:
                # We use a short timeout for quick spinner updates.
                r = self.session.get(self.base_url, headers=self.common_headers, verify=False, timeout=5)
                if r.status_code == 200:
                    print(f"\n{GREEN}Hooray! The router is back online and ready to party!{RESET}")
                    self.debug_print(f"Router response content: {r.text[:200]}...")
                    break
            except Exception as e:
                self.debug_print(f"Router status check exception: {e}")

            elapsed = time.time() - start_time
            if elapsed > timeout:
                print(f"\n{RED}Oh no! The router took too long to wake up... Timeout reached.{RESET}")
                break

            # Print spinner with a humorous message
            print(f"{YELLOW}Checking router status {spinner[spin_index % len(spinner)]} (Elapsed: {int(elapsed)} sec){RESET}", end='\r')
            spin_index += 1
            time.sleep(1)

    def run(self):
        """Runs the reboot task once."""
        print(f"{BLUE}Welcome to the Router Rebooter 3000 - Because routers need naps too!{RESET}\n")
        self.reboot()
