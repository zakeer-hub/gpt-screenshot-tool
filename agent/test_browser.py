from selenium import webdriver
from selenium.webdriver.chrome.options import Options


options = Options()

options.add_experimental_option(
    "debuggerAddress",
    "127.0.0.1:9222"
)

driver = webdriver.Chrome(options=options)

print("✅ Connected to Chrome!")

print("\nCurrent page:")
print(driver.current_url)

print("\nOpen tabs:")

for handle in driver.window_handles:

    driver.switch_to.window(handle)

    print("Title:", driver.title)
    print("URL:", driver.current_url)