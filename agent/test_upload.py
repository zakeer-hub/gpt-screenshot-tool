from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from PIL import Image, ImageDraw

import os


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
# Create a temporary test image
# -----------------------------------

test_image = os.path.abspath("test_upload.png")

image = Image.new(
    "RGB",
    (600, 300),
    "white"
)

draw = ImageDraw.Draw(image)

draw.text(
    (50, 120),
    "GPT Screenshot Tool Test",
    fill="black"
)

image.save(test_image)

print("🖼️ Test image created")


# -----------------------------------
# Find image upload input
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
# Upload image
# -----------------------------------

if image_input is None:

    print("❌ Image upload input not found")

else:

    image_input.send_keys(test_image)

    print("📎 Image attached successfully!")


print("\n👀 Check your ChatGPT window.")

input("\nPress ENTER to finish the test...")

# Remove temporary file
if os.path.exists(test_image):
    os.remove(test_image)

print("🧹 Temporary test image removed.")