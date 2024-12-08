import pytest
import time
import subprocess
import signal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests  # To check if the server is running

class Test4test:
    # Start the server before the tests
    def setup_method(self, method):
        # Ensure this is the correct directory path
        self.project_directory = "C:/Users/Андрей/Downloads/cse270/teton/1.6"  # Update this path to your actual directory

        # Start the server (assuming you're using python -m http.server to start it)
        self.server_process = subprocess.Popen(["python", "-m", "http.server", "5500"], cwd=self.project_directory)
        
        # Wait for the server to start
        self.wait_for_server("http://127.0.0.1:5500", timeout=15)

        # Setup Selenium
        options = Options()
        # options.add_argument("--headless")  # Uncomment if headless mode is necessary
        self.driver = webdriver.Chrome(options=options)
        self.vars = {}

    def wait_for_server(self, url, timeout=15):
        """Wait for the server to be ready before proceeding with the tests."""
        start_time = time.time()
        while True:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    print(f"Server is up and running at {url}")
                    break
            except requests.ConnectionError:
                pass
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Server not available at {url} after {timeout} seconds.")
            time.sleep(1)

    def teardown_method(self, method):
        # Stop the server
        if hasattr(self, 'server_process'):
            self.server_process.terminate()  # Use terminate instead of sending SIGINT

        # Close the driver
        if hasattr(self, 'driver'):
            self.driver.quit()

    def test_smokeside(self):
        self.driver.get("http://127.0.0.1:5500/teton/1.6/")
        self.driver.set_window_size(1361, 738)
        # Add assertions for the test as needed
