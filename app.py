from flask import Flask, render_template, Response
from ultralytics import YOLO
import cv2
import time

app = Flask(__name__)

model = YOLO("yolov8n.pt")
camera = cv2.VideoCapture(0)

last_detect_time = "ยังไม่พบคน"
person_count = 0

def generate_frames():
    global last_detect_time, person_count

    while True:
        success, frame = camera.read()

        if not success:
            break

        results = model(frame, verbose=False)

        person_count = 0

        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            class_name = model.names[cls_id]

            if class_name == "person":
                person_count += 1
                last_detect_time = time.strftime("%H:%M:%S")

        annotated_frame = results[0].plot()

        ret, buffer = cv2.imencode(".jpg", annotated_frame)
        frame = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
        )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video")
def video():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/status")
def status():
    return {
        "person_count": person_count,
        "last_detect_time": last_detect_time
    }

if __name__ == "__main__":
    app.run(debug=True)