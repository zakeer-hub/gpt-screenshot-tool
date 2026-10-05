from selenium import webdriver
from selenium.webdriver.chrome.options import Options


options = Options()

options.add_experimental_option(
    "debuggerAddress",
    "127.0.0.1:9222"
)

driver = webdriver.Chrome(options=options)

print("✅ Connected to ChatGPT")

print("\nButtons found:")

buttons = driver.find_elements("tag name", "button")

for button in buttons:

    try:
        text = button.text.strip()

        aria = button.get_attribute("aria-label")

        title = button.get_attribute("title")

        if text or aria or title:

            print(
                f"TEXT={text!r} | "
                f"ARIA={aria!r} | "
                f"TITLE={title!r}"
            )

    except Exception:
        pass


print("\nFile inputs found:")

inputs = driver.find_elements(
    "css selector",
    "input[type='file']"
)

print("Count:", len(inputs))