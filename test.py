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

import platform

print("=== Debug Test ===")

# Simulate your crawler's approach
options = Options()

# Use a clean temporary profile
if platform.system() == "Windows":
    profile_path = os.path.join(os.getcwd(), "chrome_profile")
else:
    profile_path = tempfile.mkdtemp(prefix="chrome_")

#clean_dir = '/Users/zen/Library/Application Support/Google/Chrome/Profile 2'  # Update this to a clean profile path if needed

os.makedirs(profile_path, exist_ok=True)

print(f"Profile dir: {profile_path}")
options.add_argument(f"--user-data-dir={profile_path}")
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