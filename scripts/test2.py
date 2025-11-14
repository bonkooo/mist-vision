import cv2
import json
from ultralytics import YOLO
import torch

print(torch.__version__, torch.cuda.is_available())

# Load image
img = cv2.imread('testSlika.jpg')
if img is None:
    print("Error: Image not found!")
    exit()

# Load YOLO model
model = YOLO("yolo11m.pt")

# Run inference
results = model(img)

# Extract detections from first (and only) frame
detections = results[0]  # YOLO result object

objs = []  # will become JSON

# Each detection is stored inside detections.boxes
for box in detections.boxes:
    # box.xyxy → tensor [[x1, y1, x2, y2]]
    xyxy = box.xyxy[0].cpu().numpy().tolist()
    x1, y1, x2, y2 = xyxy

    width = x2 - x1
    height = y2 - y1

    cls_id = int(box.cls[0])
    class_name = model.names[cls_id]

    conf = float(box.conf[0])

    obj = {
        "class": class_name,
        "confidence": round(conf,2),
        "x": round(float(x1),2),
        "y": round(float(x1),2),
        "width": round(float(x1),2),
        "height": round(float(x1),2)
    }

    objs.append(obj)

# Save JSON
with open("detections.json", "w") as f:
    json.dump(objs, f, indent=4)

print("Saved detections to detections.json")

# Show annotated frame
annotated_img = results[0].plot()
scale = 0.5
small_frame = cv2.resize(annotated_img, None, fx=scale, fy=scale)

cv2.imshow('YOLO Detection', small_frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
