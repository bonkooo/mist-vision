import cv2
import json
import os
from ultralytics import YOLO
import torch

print(torch.__version__, torch.cuda.is_available())

# ----------------------------
# CONFIG
# ----------------------------
VIDEO_PATH = "videos/testVideo.mp4"
FRAME_OUTPUT = "frames"
JSON_OUTPUT = "jsons"
SKIP = 180
CLASSES = [2, 5, 7]    # car, bus, truck
MODEL_PATH = "yolo11m.pt"
# ----------------------------

# Make folders
os.makedirs(FRAME_OUTPUT, exist_ok=True)
os.makedirs(JSON_OUTPUT, exist_ok=True)

# Load model
model = YOLO(MODEL_PATH)

# Open video
cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("❌ ERROR: Could not open video.")
    exit()

frame_id = 0
save_id = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video or cannot read frame.")
        break

    # Only process every SKIP-th frame
    if frame_id % SKIP == 0:
        # -------------------------
        # 1️⃣ Save image frame
        # -------------------------
        img_filename = f"frame_{save_id:04d}.jpg"
        img_path = os.path.join(FRAME_OUTPUT, img_filename)
        cv2.imwrite(img_path, frame)
        print("Saved image:", img_path)

        # -------------------------
        # 2️⃣ Run YOLO
        # -------------------------
        results = model(frame, classes=CLASSES)
        detections = results[0]

        objs = []

        for box in detections.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().tolist()

            objs.append({
                "class": model.names[int(box.cls[0])],
                "confidence": float(box.conf[0]),
                "x": float(x1),
                "y": float(y1),
                "width": float(x2 - x1),
                "height": float(y2 - y1)
            })

        # -------------------------
        # 3️⃣ Save JSON
        # -------------------------
        json_filename = f"frame_{save_id:04d}.json"
        json_path = os.path.join(JSON_OUTPUT, json_filename)

        with open(json_path, "w") as f:
            json.dump(objs, f, indent=4)

        print("Saved JSON:", json_path)

        save_id += 1

    frame_id += 1

cap.release()
print("\n🎉 Done! Total frames saved:", save_id)
