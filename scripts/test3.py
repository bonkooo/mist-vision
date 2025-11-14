import cv2
import json
import os
from ultralytics import YOLO
import torch
import sys
import numpy as np
from haze_removal import remove_fog

VIDEO_PATH = r"testVideo.mp4"
OUTPUT_IMG_FOLDER = "frames"
OUTPUT_JSON_FOLDER = "jsons"
FRAME_SKIP = 60              
CLASSES_TO_DETECT = [2, 5, 7]  # car, bus, truck
MODEL_PATH = "yolo11m.pt"

os.makedirs(OUTPUT_IMG_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_JSON_FOLDER, exist_ok=True)

if not os.path.exists(MODEL_PATH):
    print("yolo model not found")
    sys.exit(1)
model = YOLO(MODEL_PATH)

# Open video
if not os.path.exists(VIDEO_PATH):
    print("video not found")
    sys.exit(1)

cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print("video can't be opened")
    sys.exit(1)

frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print("total frames in video:", frame_count)

frame_id = 0
save_id = 0

# simple matrix for the sharpening filter
sharpen_kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])

while frame_id < frame_count:
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
    ret, frame = cap.read()
    if not ret:
        print(f"failed to read frame at ID: {frame_id}")
        break


    # apply filter
    #frame_sharp = cv2.filter2D(frame, -1, sharpen_kernel)
    img1_filename = os.path.join(OUTPUT_IMG_FOLDER, f"frame_test_{save_id:04d}.jpg")
    img_filename = os.path.join(OUTPUT_IMG_FOLDER, f"frame_{save_id:04d}.jpg")
    resized_frame = cv2.resize(frame, (500,300), interpolation=cv2.INTER_AREA)
    frame_sharp = remove_fog(resized_frame)

    # save the sharpened frame
    cv2.imwrite(img_filename, frame_sharp)
    print("Saved image:", img_filename)

    # YOLO detection
    results = model(frame_sharp, classes=CLASSES_TO_DETECT)
    detections = results[0]

    detections_list = []
    for box in detections.boxes:
        xyxy = box.xyxy[0].cpu().numpy().tolist()
        x1, y1, x2, y2 = xyxy
        width = x2 - x1
        height = y2 - y1
        cls_id = int(box.cls[0])
        class_name = model.names[cls_id]
        conf = float(box.conf[0])

        detections_list.append({
            "class": class_name,
            "confidence": round(conf, 3),
            "x": round(float(x1), 2),
            "y": round(float(y1), 2),
            "width": round(float(width), 2),
            "height": round(float(height), 2)
        })

    # Save JSON with frame order and nested detections
    json_data = {
        "frame_order": frame_id,
        "detections": detections_list
    }

    json_filename = os.path.join(OUTPUT_JSON_FOLDER, f"frame_{save_id:04d}.json")
    with open(json_filename, "w") as f:
        json.dump(json_data, f, indent=4)
    print("Saved JSON:", json_filename)


    save_id += 1
    frame_id += FRAME_SKIP  # jump to next frame to save

cap.release()
print("finished")
