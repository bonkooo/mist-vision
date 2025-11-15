import cv2
import os
import json
import numpy as np
import time
from ultralytics import YOLO
from haze_removal import remove_fog  # your function

# For audio alert
try:
    import winsound
    AUDIO_AVAILABLE = True
except:
    AUDIO_AVAILABLE = False

# === CONFIGURATION ===
VIDEO_PATH = "treciPrimer_gustaMagla_cut.mp4"
OUTPUT_VIDEO = "treciPrimer_processed.mp4"
OUTPUT_JSON_DIR = "frame_json"
MODEL_PATH = "yolo11m.pt"
CLASSES_TO_DETECT = [2, 5, 7]  # car, bus, truck
IMG_SIZE = (640, 384)

# --- Distance tuning parameter ---
# Increase = must be closer to turn red
# Decrease = alert activates earlier
CLOSE_THRESHOLD = 11000

# Alert text
WARNING_TEXT = "          !!!"

os.makedirs(OUTPUT_JSON_DIR, exist_ok=True)



# === Helper: Draw warning overlay ===
def draw_warning(frame):
    cv2.putText(frame, WARNING_TEXT, (30, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 0, 255), 4)


# === Helper: draw colored distance-based boxes ===
def draw_boxes_distance(frame, detections, danger_detected=False):
    for box in detections.boxes:
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)

        width = x2 - x1
        height = y2 - y1
        area = width * height

        if area >= CLOSE_THRESHOLD:
            color = (0, 0, 255)  # RED = CLOSE
            danger_detected = True
        else:
            color = (0, 255, 255)  # YELLOW = FAR

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    return frame, danger_detected


def process_video():
    if not os.path.exists(VIDEO_PATH):
        raise FileNotFoundError("Input video not found.")

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("YOLO model not found.")

    print("Loading YOLO model...")
    model = YOLO(MODEL_PATH)

    cap = cv2.VideoCapture(VIDEO_PATH)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"FPS: {fps} | Frames: {total_frames}")

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, fps, IMG_SIZE)

    frame_id = 0
    json_id = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, IMG_SIZE)
        frame_filtered = remove_fog(frame)

        results = model(frame_filtered, classes=CLASSES_TO_DETECT)
        detections = results[0]

        # === JSON EXPORT ===
        det_list = []
        for box in detections.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().tolist()
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            name = model.names[cls]

            det_list.append({
                "class": name,
                "confidence": round(conf, 3),
                "x": round(x1, 2),
                "y": round(y1, 2),
                "width": round(x2-x1, 2),
                "height": round(y2-y1, 2),
            })

        json_data = {"frame": frame_id, "detections": det_list}
        json_path = os.path.join(OUTPUT_JSON_DIR, f"frame_{json_id:04d}.json")
        with open(json_path, "w") as f:
            json.dump(json_data, f, indent=4)

        # === DRAW BOXES (yellow/red based on distance) ===
        danger = False
        drawn_frame, danger = draw_boxes_distance(frame_filtered.copy(), detections, danger)

        # === WARNING TEXT + SOUND ===
        if danger:
            draw_warning(drawn_frame)

        last_danger = danger

        # Save video
        out.write(drawn_frame)
        print(f"Processed frame {frame_id}/{total_frames}", end="\r")

        frame_id += 1
        json_id += 1

    cap.release()
    out.release()
    print("\nDone!")
    print("Saved video output to:", OUTPUT_VIDEO)
    print("Saved JSON files in:", OUTPUT_JSON_DIR)


if __name__ == "__main__":
    process_video()
