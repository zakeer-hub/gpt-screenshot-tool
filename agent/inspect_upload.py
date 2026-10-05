from selenium import webdriver
from selenium.webdriver.chrome.options import Options


options = Options()

options.add_experimental_option(
    "debuggerAddress",
    "127.0.0.1:9222"
)

driver = webdriver.Chrome(options=options)

print("✅ Connected to ChatGPT")

file_inputs = driver.find_elements(
    "css selector",
    "input[type='file']"
)

print(f"\nFound {len(file_inputs)} file inputs:\n")


for index, element in enumerate(file_inputs, start=1):

    print(f"--- File input {index} ---")

    print("accept:", element.get_attribute("accept"))
    print("multiple:", element.get_attribute("multiple"))
    print("name:", element.get_attribute("name"))
    print("id:", element.get_attribute("id"))
    print("displayed:", element.is_displayed())

    print()