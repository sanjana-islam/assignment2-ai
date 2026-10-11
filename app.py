from flask import Flask, render_template, request
import os
import requests

app = Flask(__name__)

# STUDENT INFO
MY_NAME = "Sanjana Islam Orthy"
MY_STUDENT_ID = "2026512866"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""
    question = ""
    if request.method == "POST":
        question = request.form.get("question", "")
        if not GEMINI_API_KEY:
            answer = "⚠️ ERROR: GEMINI_API_KEY not set. Go to Render Dashboard > Environment > Add your Gemini API key."
        elif question:
            try:
                # LATEST MODEL - gemini-3.8-flash (2.0 is no longer available)
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={GEMINI_API_KEY}"
                payload = {"contents": [{"parts": [{"text": question}]}]}
                headers = {"Content-Type": "application/json"}

                resp = requests.post(url, json=payload, headers=headers, timeout=30)
                data = resp.json()

                if 'candidates' in data and len(data['candidates']) > 0:
                    answer = data['candidates'][0]['content']['parts'][0]['text']
                else:
                    answer = f"API Response: {data}"

            except Exception as e:
                answer = f"AI API Error: {e}"

    return render_template("index.html", name=MY_NAME, sid=MY_STUDENT_ID, answer=answer, question=question)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
