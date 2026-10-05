const targetUrl = document.getElementById("targetUrl");
const connectBtn = document.getElementById("connectBtn");
const status = document.getElementById("status");

connectBtn.addEventListener("click", async () => {

    const url = targetUrl.value.trim();

    if (!url) {
        status.textContent = "🔴 Please enter a ChatGPT URL.";
        return;
    }

    if (!url.startsWith("https://chatgpt.com/")) {
        status.textContent = "🔴 Please enter a valid ChatGPT URL.";
        return;
    }

    try {

        const response = await fetch("http://127.0.0.1:8765/target", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                url: url
            })
        });

        const data = await response.json();

        if (data.success) {

            localStorage.setItem("targetChatGPTUrl", url);

            status.textContent =
                "🟢 ChatGPT conversation connected.";

            console.log("Target sent to Python:", url);

        } else {

            status.textContent =
                "🔴 Could not connect.";

        }

    } catch (error) {

        console.error(error);

        status.textContent =
            "🔴 Python agent is not reachable.";

    }
});


const savedUrl = localStorage.getItem("targetChatGPTUrl");

if (savedUrl) {
    targetUrl.value = savedUrl;
}

const screenshotPreview =
    document.getElementById("screenshotPreview");


async function checkForScreenshot() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8765/screenshot"
        );

        const data = await response.json();

        if (data.image) {

            screenshotPreview.src =
                data.image;

            screenshotPreview.style.display =
                "block";
        }

    } catch (error) {

        // Python agent may not be running.
    }
}


setInterval(checkForScreenshot, 1000);