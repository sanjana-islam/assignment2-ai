M# STUDENT INFO
Y_NAME = "Sanjana Islam Orthy"
MY_STUDENT_ID = "2026512866"

import os
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head><title>Render-based Cloud Service with AI Feature</title>
<style>
body{background:#f5f7fb;font-family:Arial;display:flex;justify-content:center;padding:30px}
.card{background:white;padding:25px;border-radius:12px;width:650px;box-shadow:0 4px 15px rgba(0,0,0,0.1)}
h2{color:#1a73e8;text-align:center}
.info{background:#e8f0fe;padding:12px;border-left:4px solid #1a73e8;border-radius:6px;margin:15px 0}
input{width:100%;padding:12px;border:1px solid #ccc;border-radius:8px;margin:10px 0;box-sizing:border-box}
button{background:#1a73e8;color:white;padding:10px 20px;border:none;border-radius:6px;cursor:pointer}
.answer{background:#f1f1f1;padding:12px;border-radius:8px;margin-top:15px;white-space:pre-wrap}
.small{font-size:11px;color:gray;text-align:center;margin-top:15px}
</style>
</head>
<body>
<div class="card">
<h2>Render-based Cloud Service with AI Feature</h2>
<div class="info">
<b>Name:</b> Sanjana Islam Orthy<br>
<b>Student ID:</b> 2026512866<br>
<b>Assignment:</b> Cloud Computing - Assignment 2 (Due: 28 Sept 2026)
</div>
<h3>AI Feature: Ask Anything - Powered by Google Gemini</h3>
<form method="POST">
<input type="text" name="q" placeholder="Ask anything, e.g., What is Render?" required value="{{q}}">
<button type="submit">Ask AI</button>
</form>
{% if ans %}
<div class="answer"><b>AI Answer:</b><br>{{ans}}</div>
{% endif %}
<div class="small">This AI feature uses external API token: GEMINI_API_KEY (Google Gemini API gemini-2.5-flash)<br>Deployed on Render.com Free Tier</div>
</div>
</body>
</html>
"""

def ask_ai(question):
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return "ERROR: GEMINI_API_KEY not set in Render Environment."
    for model in ["gemini-2.5-flash", "gemini-2.0-flash"]:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
            r = requests.post(url, json={"contents":[{"parts":[{"text":question}]}]}, timeout=30)
            j = r.json()
            if "candidates" in j:
                return j["candidates"][0]["content"]["parts"][0]["text"]
        except:
            continue
    return f"Error: {j}"

@app.route("/", methods=["GET","POST"])
def home():
    ans = ""
    q = ""
    if request.method == "POST":
        q = request.form.get("q","")
        ans = ask_ai(q)
    return render_template_string(HTML, ans=ans, q=q)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
