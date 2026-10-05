from selenium import webdriver
from selenium.webdriver.chrome.options import Options


options = Options()

options.add_experimental_option(
    "debuggerAddress",
    "127.0.0.1:9222"
)

driver = webdriver.Chrome(options=options)

print("✅ Connected to ChatGPT")

print("\nPossible SEND buttons:\n")

buttons = driver.find_elements("tag name", "button")

for index, button in enumerate(buttons, start=1):

    try:
        aria = button.get_attribute("aria-label")
        title = button.get_attribute("title")
        button_type = button.get_attribute("type")
        text = button.text.strip()

        if (
            (aria and "send" in aria.lower())
            or
            (title and "send" in title.lower())
            or
            button_type == "submit"
        ):

            print(f"Button {index}")
            print("  text:", repr(text))
            print("  aria:", repr(aria))
            print("  title:", repr(title))
            print("  type:", repr(button_type))
            print()

    except Exception:
        pass


print("\nButtons near the composer:\n")

for index, button in enumerate(buttons, start=1):

    try:

        aria = button.get_attribute("aria-label")

        if aria in [
            "Add files and more",
            "Dictate",
            "Start Voice",
            "Send message",
            "Send prompt"
        ]:

            print(
                f"{index}: "
                f"{aria}"
            )

    except Exception:
        pass