import os
import subprocess
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Test4test():
    def setup_method(self, method):
        # Set up the project directory
        self.project_directory = os.path.join(os.getcwd(), "teton", "1.6")
        
        # Start the server on a different port to avoid conflicts
        self.server_process = subprocess.Popen(
            ["python", "-m", "http.server", "5501"], cwd=self.project_directory
        )
        
        # Wait for the server to start
        self.wait_for_server("http://127.0.0.1:5501", timeout=15)
        
        # Set up Selenium WebDriver
        options = Options()
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        # Uncomment for headless mode
        # options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()
        self.server_process.terminate()

    def wait_for_server(self, url, timeout=15):
        import time
        import requests
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    print(f"Server is up and running at {url}")
                    return
            except requests.ConnectionError:
                time.sleep(1)
        raise RuntimeError(f"Server did not start within {timeout} seconds")

    def test_directorypage(self):
        self.driver.get("http://127.0.0.1:5501/teton/1.6/index.html")
        self.driver.set_window_size(1361, 738)
        
        # Wait for the "Directory" link to be clickable
        directory_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Directory"))
        )
        directory_link.click()
        
        # Wait for the gold member element to be present
        gold_member = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".gold-member:nth-child(9) > p:nth-child(2)"))
        )
        assert gold_member.text == "Teton Turf and Tree"