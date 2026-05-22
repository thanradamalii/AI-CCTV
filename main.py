from ultralytics import YOLO
import cv2
import requests
import time

# =====================
# WEBSITE
# =====================

UPLOAD_URL = "https://thanradamalii.pythonanywhere.com/upload"

# =====================
# TELEGRAM
# =====================

BOT_TOKEN = "8845494473:AAFNpm-o0Ftiuj0YM1AwuPDKnG7n2yLALc4"
CHAT_ID = "7225797495"

# =====================
# AI MODEL
# =====================

model = YOLO("yolov8n.pt")

camera = cv2.VideoCapture(0)

last_alert_time = 0
ALERT_COOLDOWN = 10

# =====================
# FUNCTIONS
# =====================

def send_telegram_message(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        requests.post(url,data=data)
        print("Telegram Sent")

    except Exception as error:
        print(error)

def upload_image(image_path):

    try:

        with open(image_path,"rb") as file:

            files = {
                "image": file
            }

            data = {
                "type":"Person Detected"
            }

            response = requests.post(
                UPLOAD_URL,
                files=files,
                data=data
            )

            print(response.text)

    except Exception as error:
        print(error)

# =====================
# MAIN LOOP
# =====================

while True:

    ret, frame = camera.read()

    if not ret:
        break

    results = model(frame, verbose=False)

    person_detected = False

    for box in results[0].boxes:

        cls_id = int(box.cls[0])

        class_name = model.names[cls_id]

        if class_name == "person":

            person_detected = True

    annotated_frame = results[0].plot()

    if person_detected:

        current_time = time.time()

        if current_time - last_alert_time > ALERT_COOLDOWN:

            image_path = "latest.jpg"

            cv2.imwrite(image_path, annotated_frame)

            upload_image(image_path)

            send_telegram_message(
                "🚨 ตรวจพบคนจากระบบ AI CCTV"
            )

            last_alert_time = current_time

    cv2.imshow("AI CCTV", annotated_frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

camera.release()
cv2.destroyAllWindows()