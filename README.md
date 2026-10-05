# GPT Screenshot Tool 📸

A desktop automation tool that captures your screen with a keyboard shortcut and automatically uploads the screenshot to an already-open ChatGPT conversation.

## ✨ Features

- 📸 Capture full-screen screenshots
- ⌨️ Global shortcut: `Ctrl + Shift + Y`
- 🤖 Automatically connect to Chrome
- 📎 Automatically attach screenshot to ChatGPT
- 🚀 Automatically send the screenshot
- 💾 No need to manually save the screenshot
- 🌐 Simple web interface for selecting the target ChatGPT conversation

## 🛠️ Technologies

- Python
- Flask
- Selenium
- MSS
- Keyboard
- HTML
- CSS
- JavaScript
- Chrome Remote Debugging

## 📁 Project Structure

```text
gpt-screenshot-tool/
│
├── agent/
│   ├── main.py
│   ├── test_browser.py
│   ├── test_upload.py
│   ├── test_real_upload.py
│   ├── inspect_chatgpt.py
│   ├── inspect_upload.py
│   └── agent/
│       ├── inspect_send.py
│       └── send_test.py
│
├── index.html
├── style.css
├── app.js
└── .gitignore
