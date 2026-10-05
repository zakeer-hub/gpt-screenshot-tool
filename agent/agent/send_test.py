from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


options = Options()

options.add_experimental_option(
    "debuggerAddress",
    "127.0.0.1:9222"
)

driver = webdriver.Chrome(options=options)

print("✅ Connected to ChatGPT")


send_button = driver.find_element(
    "css selector",
    "button[aria-label='Send']"
)

print("🚀 Send button found")

time.sleep(2)

send_button.click()

print("✅ Message sent!")