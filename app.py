import os, requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML = """[your existing HTML - keep same]"""
# OR just keep your old HTML, only replace the Python function below

def ask_gemini(question):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "ERROR: GEMINI_API_KEY not set."

    models = ["gemini-2.5-flash", "gemini-1.5-flash-latest", "gemini-pro"]
    for model in models:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            data = {"contents": [{"parts": [{"text": question}]}]}
            r = requests.post(url, json=data, timeout=20)
            j = r.json()
            if "candidates" in j:
                return j["candidates"][0]["content"]["parts"][0]["text"]
        except:
            continue
    return f"AI API Error: {j}"

@app.route("/", methods=["GET","POST"])
def home():
    answer = ""
    if request.method == "POST":
        q = request.form.get("question","")
        answer = ask_gemini(q)
    # render your existing page with answer
    return render_template_string(open("templates/index.html").read() if os.path.exists("templates/index.html") else HTML, answer=answer)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
    
