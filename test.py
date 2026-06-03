# test_crawler_debug.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import logging
logging.basicConfig(level=logging.DEBUG)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import tempfile

print("=== Debug Test ===")

# Simulate your crawler's approach
options = Options()

# Use a clean temporary profile
clean_dir = '/Users/zen/Library/Application Support/Google/Chrome/Profile 2'  # Update this to a clean profile path if needed
print(f"Profile dir: {clean_dir}")
options.add_argument(f"--user-data-dir={clean_dir}")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

print("Creating driver...")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

print("Driver created! Navigating...")
driver.get("https://www.financialjuice.com")
print(f"Title: {driver.title}")

driver.quit()
print("Success!")