
import os
import logging
from flask import Flask, request, jsonify, render_template_string
from google import genai

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

HTML = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>JARVIS AI</title>
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    background: #080d16;
    color: #00e5ff;
    font-family: Tahoma, sans-serif;
}
.container {
    max-width: 700px;
    margin: 35px auto;
    padding: 18px;
}
h1 { text-align: center; font-size: 38px; }
.status { text-align: center; color: #5cff9d; }
#chat {
    background: #111c2b;
    border: 1px solid #00e5ff;
    border-radius: 15px;
    padding: 15px;
    height: 400px;
    overflow-y: auto;
    color: white;
}
.message {
    margin: 14px 0;
    white-space: pre-wrap;
    line-height: 1.8;
}
.input-area {
    display: flex;
    gap: 8px;
    margin-top: 15px;
}
input {
    flex: 1;
    min-width: 0;
    padding: 14px;
    border-radius: 10px;
    border: 1px solid #00e5ff;
    background: #111c2b;
    color: white;
}
button {
    padding: 14px 20px;
    border: 0;
    border-radius: 10px;
    background: #00c8e5;
    cursor: pointer;
    font-weight: bold;
}
button:disabled { opacity: .5; }
</style>
</head>
<body>
<div class="container">
    <h1>J.A.R.V.I.S</h1>
    <p class="status">● ONLINE</p>
    <div id="chat">
        <div class="message">JARVIS: سلام! من آماده‌ام. چه کاری برات انجام بدم؟</div>
    </div>
    <div class="input-area">
        <input id="message" placeholder="پیامت را بنویس...">
        <button id="send" onclick="sendMessage()">ارسال</button>
    </div>
</div>

<script>
const chat = document.getElementById("chat");
const input = document.getElementById("message");
const button = document.getElementById("send");

function addMessage(who, text) {
    const p = document.createElement("div");
    p.className = "message";
    p.textContent = who + ": " + text;
    chat.appendChild(p);
    chat.scrollTop = chat.scrollHeight;
}

async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    input.value = "";
    addMessage("شما", message);

    button.disabled = true;
    button.textContent = "در حال فکر کردن...";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message})
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.reply || "خطا در پاسخ");
        }

        addMessage("JARVIS", data.reply);

    } catch (error) {
        addMessage("خطا", error.message);
    } finally {
        button.disabled = false;
        button.textContent = "ارسال";
        input.focus();
    }
}

input.addEventListener("keydown", function(e) {
    if (e.key === "Enter") sendMessage();
});
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/health")
def health():
    return jsonify({"status": "online"})


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}
        message = str(data.get("message", "")).strip()

        if not message:
            return jsonify({"reply": "لطفاً پیام بنویس."}), 400

        if len(message) > 4000:
            return jsonify({"reply": "پیامت خیلی طولانی است."}), 400

        api_key = os.environ.get("GEMINI_API_KEY")

        if not api_key:
            return jsonify({
                "reply": "کلید هوش مصنوعی در تنظیمات Render پیدا نشد."
            }), 500

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=[
                "تو Jarvis هستی، دستیار هوشمند و دوستانه. "
                "به فارسی روان پاسخ بده. پاسخ‌ها دقیق و مفید باشند.",
                message
            ]
        )

        answer = response.text

        if not answer:
            answer = "پاسخی دریافت نکردم. دوباره تلاش کن."

        return jsonify({"reply": answer})

    except Exception:
        logging.exception("Gemini request failed")
        return jsonify({
            "reply": "اتصال به هوش مصنوعی مشکل دارد. گزارش Render را بررسی کن."
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
