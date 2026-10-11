from flask import Flask, render_template, request
import os
import requests
import psycopg2
app = Flask(__name__)

# STUDENT INFO
MY_NAME = "Sanjana Islam Orthy"
MY_STUDENT_ID = "2026512866"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    if not DATABASE_URL:
        return None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except:
        return None

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
                # FIXED: 1.5 -> 2.0-flash
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
                payload = {"contents": [{"parts": [{"text": question}]}]}
                resp = requests.post(url, json=payload, timeout=30)
                data = resp.json()

                # Error check
                if 'candidates' in data:
                    answer = data['candidates'][0]['content']['parts'][0]['text']
                else:
                    answer = f"API Error: {data}"

            except Exception as e:
                answer = f"AI API Error: {e}"
    return render_template("index.html", name=MY_NAME, sid=MY_STUDENT_ID, answer=answer, question=question)

@app.route("/db-test")
def db_test():
    if not DATABASE_URL:
        return "DATABASE_URL not set in Render Environment - Please add it"
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT NOW();')
        time = cur.fetchone()
        cur.close()
        conn.close()
        return f"✅ Database Connected Successfully! Time: {time[0]}"
    except Exception as e:
        return f"❌ DB Error: {e}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

