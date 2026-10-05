from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import mss
import os

from PIL import Image


# -----------------------------------
# Connect to existing Chrome
# -----------------------------------

options = Options()

options.add_experimental_option(
    "debuggerAddress",
    "127.0.0.1:9222"
)

driver = webdriver.Chrome(options=options)

print("✅ Connected to ChatGPT")


# -----------------------------------
# Capture real screen
# -----------------------------------

temp_file = os.path.abspath("temp_screenshot.jpg")

with mss.MSS() as sct:

    screenshot = sct.grab(sct.monitors[1])

    image = Image.frombytes(
        "RGB",
        screenshot.size,
        screenshot.rgb
    )

    image.save(
        temp_file,
        format="JPEG",
        quality=85
    )

print("📸 Real screenshot captured")


# -----------------------------------
# Find ChatGPT image upload input
# -----------------------------------

file_inputs = driver.find_elements(
    "css selector",
    "input[type='file']"
)

image_input = None

for element in file_inputs:

    accept = element.get_attribute("accept")

    if accept == "image/*":

        image_input = element
        break


# -----------------------------------
# Attach screenshot
# -----------------------------------

if image_input is None:

    print("❌ Image upload input not found")

else:

    image_input.send_keys(temp_file)

    print("📎 Real screenshot attached successfully!")


# -----------------------------------
# Wait for ChatGPT upload
# -----------------------------------

print("\n⏳ Waiting for ChatGPT upload to finish...")

import time

time.sleep(10)

print("👀 Check ChatGPT for upload result.")

input("\nPress ENTER to finish...")


# -----------------------------------
# Delete after upload test
# -----------------------------------

if os.path.exists(temp_file):

    os.remove(temp_file)

    print("🧹 Temporary screenshot deleted")