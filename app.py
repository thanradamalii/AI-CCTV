from flask import Flask, render_template, request, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
LATEST_IMAGE = os.path.join(UPLOAD_FOLDER, "latest.jpg")
HISTORY_FILE = os.path.join(UPLOAD_FOLDER, "history.json")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=2)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():

    image = request.files.get("image")
    detected_type = request.form.get("type", "Person Detected")

    if not image:
        return "No image", 400

    image.save(LATEST_IMAGE)

    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    history = load_history()

    history.insert(0, {
        "time": now,
        "type": detected_type
    })

    history = history[:20]

    save_history(history)

    return "Upload Success"

@app.route("/status")
def status():

    history = load_history()

    return jsonify({
        "latest_image": "/static/uploads/latest.jpg",
        "last_detect_time": history[0]["time"] if history else "-",
        "last_detect_type": history[0]["type"] if history else "-",
        "history": history
    })

if __name__ == "__main__":
    app.run(debug=True)