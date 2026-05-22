from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    image = request.files.get("image")

    if image:
        image.save(os.path.join(UPLOAD_FOLDER, "latest.jpg"))
        return "upload success"

    return "no image", 400