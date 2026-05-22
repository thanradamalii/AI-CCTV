from ultralytics import YOLO
import cv2
import requests
import time

# =========================
# Telegram Setting
# =========================

BOT_TOKEN = "8845494473:AAFNpm-o0Ftiuj0YM1AwuPDKnG7n2yLALc4"
CHAT_ID = "7225797495"

last_alert_time = 0

# =========================
# Send Telegram Message
# =========================

def send_telegram_message(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)

# =========================
# AI Model
# =========================

model = YOLO("yolov8n.pt")

cam = cv2.VideoCapture(0)

# =========================
# Main Loop
# =========================

while True:

    ret, frame = cam.read()

    if not ret:
        break

    results = model(frame, verbose=False)

    # ตรวจจับ object
    for box in results[0].boxes:

        cls_id = int(box.cls[0])

        class_name = model.names[cls_id]

        # ถ้าเจอคน
        if class_name == "person":

            current_time = time.time()

            # แจ้งเตือนทุก 10 วินาที
            if current_time - last_alert_time > 10:

                send_telegram_message("🚨 ตรวจพบคนจาก AI CCTV")

                print("ส่งแจ้งเตือนแล้ว")

                last_alert_time = current_time

    annotated_frame = results[0].plot()

    cv2.imshow("AI CCTV", annotated_frame)

    # กด ESC เพื่อปิด
    if cv2.waitKey(1) & 0xFF == 27:
        break

cam.release()
cv2.destroyAllWindows()