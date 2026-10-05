from flask import Flask, request, jsonify
from flask_cors import CORS

import mss
import keyboard
import time
import base64
import os
import io
import requests

from PIL import Image

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# =========================================================
# Flask setup
# =========================================================

app = Flask(__name__)
CORS(app)

target_url = None
latest_screenshot = None


# =========================================================
# Receive target ChatGPT conversation URL
# =========================================================

@app.route("/target", methods=["POST"])
def set_target():

    global target_url

    data = request.get_json()

    if not data or not data.get("url"):
        return jsonify({
            "success": False,
            "message": "ChatGPT URL missing"
        }), 400

    target_url = data["url"].strip()

    print("\n🎯 Target ChatGPT conversation:")
    print(target_url)

    return jsonify({
        "success": True,
        "target": target_url
    })


# =========================================================
# Status
# =========================================================

@app.route("/status", methods=["GET"])
def status():

    return jsonify({
        "connected": target_url is not None,
        "target": target_url
    })


# =========================================================
# Receive screenshot from agent
# =========================================================

@app.route("/screenshot", methods=["POST"])
def receive_screenshot():

    global latest_screenshot

    file = request.files.get("image")

    if not file:

        return jsonify({
            "success": False,
            "message": "No image received"
        }), 400

    image_data = file.read()

    latest_screenshot = (
        "data:image/jpeg;base64,"
        + base64.b64encode(image_data).decode("utf-8")
    )

    print("📸 Screenshot received!")

    return jsonify({
        "success": True
    })


# =========================================================
# Website asks for latest screenshot
# =========================================================

@app.route("/screenshot", methods=["GET"])
def get_screenshot():

    return jsonify({
        "image": latest_screenshot
    })


# =========================================================
# Connect to existing Chrome
# =========================================================

def connect_to_chrome():

    options = Options()

    options.add_experimental_option(
        "debuggerAddress",
        "127.0.0.1:9222"
    )

    driver = webdriver.Chrome(
        options=options
    )

    return driver


# =========================================================
# Find / open target ChatGPT conversation
# =========================================================

def open_target_conversation(driver):

    if not target_url:

        print("❌ No ChatGPT conversation connected.")

        return False

    print("🎯 Looking for target ChatGPT tab...")

    # Check currently open tabs
    for handle in driver.window_handles:

        try:

            driver.switch_to.window(handle)

            current_url = driver.current_url

            if current_url == target_url:

                print("✅ Target conversation tab found.")

                return True

        except Exception:

            pass

    # If exact tab wasn't found, open target URL
    print("🌐 Opening target conversation...")

    driver.get(target_url)

    time.sleep(5)

    if target_url in driver.current_url:

        print("✅ Target conversation opened.")

        return True

    print("❌ Could not open target conversation.")

    return False


# =========================================================
# Upload screenshot + send to ChatGPT
# =========================================================

def upload_to_chatgpt(file_path):

    if not target_url:

        print("❌ No ChatGPT conversation connected.")

        return False

    driver = None

    try:

        # -------------------------------------------------
        # Connect to Chrome
        # -------------------------------------------------

        print("🌐 Connecting to Chrome...")

        driver = connect_to_chrome()

        print("✅ Connected to Chrome")


        # -------------------------------------------------
        # Open target conversation
        # -------------------------------------------------

        if not open_target_conversation(driver):

            return False


        # -------------------------------------------------
        # Find image upload input
        # -------------------------------------------------

        print("🔎 Finding image upload input...")

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

        if image_input is None:

            print("❌ Image upload input not found.")

            return False


        # -------------------------------------------------
        # Upload screenshot
        # -------------------------------------------------

        print("📎 Uploading screenshot...")

        image_input.send_keys(
            os.path.abspath(file_path)
        )

        print("✅ Screenshot given to ChatGPT upload.")


        # -------------------------------------------------
        # Wait for Send button
        # -------------------------------------------------

        print("⏳ Waiting for Send button...")

        wait = WebDriverWait(
            driver,
            20
        )

        send_button = wait.until(
            EC.element_to_be_clickable(
                (
                    "css selector",
                    "button[aria-label='Send']"
                )
            )
        )

        print("✅ Send button found.")


        # -------------------------------------------------
        # Small delay for UI
        # -------------------------------------------------

        time.sleep(2)


        # -------------------------------------------------
        # Click Send
        # -------------------------------------------------

        print("🚀 Sending screenshot...")

        send_button.click()

        print("✅ Screenshot sent to ChatGPT!")

        # Give ChatGPT some time to process it
        time.sleep(5)

        return True


    except Exception as error:

        print("\n❌ ChatGPT automation error:")
        print(error)

        return False


# =========================================================
# Delete temporary file safely
# =========================================================

def delete_temp_file(temp_file):

    if not os.path.exists(temp_file):

        return

    for attempt in range(10):

        try:

            os.remove(temp_file)

            print("🧹 Temporary screenshot deleted.")

            return

        except PermissionError:

            print(
                f"⏳ Screenshot still in use... "
                f"retry {attempt + 1}/10"
            )

            time.sleep(1)

        except OSError as error:

            print(
                f"⚠️ Could not delete screenshot: {error}"
            )

            return

    print(
        "⚠️ Screenshot could not be deleted automatically."
    )


# =========================================================
# Capture screenshot
# =========================================================

def take_screenshot():

    print("\n📸 Taking screenshot...")

    temp_file = os.path.abspath(
        "temp_screenshot.jpg"
    )

    try:

        # -------------------------------------------------
        # Capture screen
        # -------------------------------------------------

        with mss.MSS() as sct:

            screenshot = sct.grab(
                sct.monitors[1]
            )

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

        print("✅ Screenshot captured!")

        print(
            f"Size: "
            f"{screenshot.width} x {screenshot.height}"
        )


        # -------------------------------------------------
        # Read screenshot into memory
        # -------------------------------------------------

        with open(
            temp_file,
            "rb"
        ) as file:

            image_data = file.read()

        print(
            f"Image size: "
            f"{len(image_data) / 1024:.2f} KB"
        )


        # -------------------------------------------------
        # Send screenshot to website preview
        # -------------------------------------------------

        try:

            response = requests.post(
                "http://127.0.0.1:8765/screenshot",
                files={
                    "image": (
                        "screenshot.jpg",
                        image_data,
                        "image/jpeg"
                    )
                },
                timeout=10
            )

            if response.status_code == 200:

                print(
                    "🖥️ Screenshot sent to website preview."
                )

            else:

                print(
                    "⚠️ Website preview returned:",
                    response.status_code
                )

        except requests.RequestException as error:

            print(
                "⚠️ Website preview failed:"
            )

            print(error)


        # -------------------------------------------------
        # Upload + send to ChatGPT
        # -------------------------------------------------

        upload_to_chatgpt(
            temp_file
        )


    except Exception as error:

        print("\n❌ Screenshot error:")
        print(error)


    finally:

        # -------------------------------------------------
        # Safe cleanup
        # -------------------------------------------------

        delete_temp_file(
            temp_file
        )


# =========================================================
# Global keyboard listener
# =========================================================

def start_keyboard_listener():

    print(
        "⌨️ Waiting for Ctrl + Shift + Y"
    )

    print(
        "Press ESC to stop"
    )

    while True:

        try:

            if keyboard.is_pressed(
                "ctrl+shift+y"
            ):

                take_screenshot()

                # Prevent repeated screenshots
                # while keys are still pressed
                time.sleep(1)


            if keyboard.is_pressed("esc"):

                print("🛑 Agent stopped.")

                break


            time.sleep(0.05)

        except Exception as error:

            print(
                "❌ Keyboard listener error:"
            )

            print(error)

            time.sleep(1)


# =========================================================
# Start application
# =========================================================

if __name__ == "__main__":

    import threading


    keyboard_thread = threading.Thread(
        target=start_keyboard_listener,
        daemon=True
    )

    keyboard_thread.start()


    print("\n🚀 GPT Screenshot Agent started")

    print(
        "⌨️ Press Ctrl + Shift + Y to capture"
    )

    print(
        "🌐 Chrome debugging port: 9222"
    )


    app.run(
        host="127.0.0.1",
        port=8765,
        debug=False
    )