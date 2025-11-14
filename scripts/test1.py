import cv2
from ultralytics import YOLO
import torch
print(torch.__version__, torch.cuda.is_available())

model = YOLO("yolo11m.pt") 

video_path = "videos/testVideo.mp4"
cap = cv2.VideoCapture(video_path)
frame_id = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if frame_id % 5 != 0:
        frame_id += 1
        continue

    results = model(frame, classes=[2, 5, 7])  
    # COCO klase:
    # 2 = car, 5 = bus, 7 = truck

    annotated_frame = results[0].plot()

    #cv2.imshow("Detekcija vozila", annotated_frame)
    scale = 0.3  # 0.5 = 50%, 0.3 = 30%, 1.0 = original

    small_frame = cv2.resize(annotated_frame, None, fx=scale, fy=scale)
    cv2.imshow("Video", small_frame)
    frame_id += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.waitKey(0)
cv2.destroyAllWindows()