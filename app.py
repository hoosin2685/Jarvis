from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>JARVIS AI</title>
<style>
body {
    margin: 0;
    background: #080d16;
    color: #00e5ff;
    font-family: Tahoma, sans-serif;
    text-align: center;
}
.container {
    max-width: 650px;
    margin: 40px auto;
    padding: 20px;
}
h1 { font-size: 38px; }
#chat {
    background: #111c2b;
    border: 1px solid #00e5ff;
    border-radius: 15px;
    padding: 15px;
    height: 350px;
    overflow-y: auto;
    text-align: right;
    color: white;
}
input {
    width: 70%;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #00e5ff;
    background: #111c2b;
    color: white;
    margin-top: 15px;
}
button {
    padding: 15px;
    border: 0;
    border-radius: 10px;
    background: #00c8e5;
    cursor: pointer;
    font-weight: bold;
}
</style>
</head>
<body>
<div class="container">
    <h1>J.A.R.V.I.S</h1>
    <p>YOUR PERSONAL AI ASSISTANT</p>
    <div id="chat">
        <p>JARVIS: سلام! من آماده‌ام.</p>
    </div>
    <input id="message" placeholder="پیامت را بنویس...">
    <button onclick="sendMessage()">ارسال</button>
</div>

<script>
async function sendMessage() {
    const input = document.getElementById("message");
    const chat = document.getElementById("chat");
    const message = input.value.trim();

    if (!message) return;

    chat.innerHTML += "<p>شما: " + message + "</p>";
    input.value = "";

    const response = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message})
    });

    const data = await response.json();
    chat.innerHTML += "<p>JARVIS: " + data.reply + "</p>";
    chat.scrollTop = chat.scrollHeight;
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    return jsonify({"reply": "پیامت دریافت شد! به‌زودی مغز هوش مصنوعی من متصل می‌شود."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
