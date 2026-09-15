import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)
API_KEY = os.environ.get("GCP_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True)
        if not data:
            user_message = request.form.get("message")
        else:
            user_message = data.get("message")

        if not user_message:
            return jsonify({"response": "Please enter a message."})

        if not model:
            return jsonify({"response": "Error: API Key is not configured."})

        response = model.generate_content(user_message)
        return jsonify({"response": response.text})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

