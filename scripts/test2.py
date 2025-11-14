import cv2
from ultralytics import YOLO
import torch
import time
print(torch.__version__, torch.cuda.is_available())
#img = cv2.imread('testSlika.jpg')
 # Display the image in a window
model = YOLO("yolo11m.pt")  # make sure this file exists in the same folder

# Otvori video (moÅ¾e i snimak sa telefona)
video_path = "magla1.mp4"
cap = cv2.VideoCapture(video_path)
frame_id = 0
save_id = 0

skip = 180

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detekcija
    results = model(frame, classes=[2, 5, 7])  
    # COCO klase:
    # 2 = car, 5 = bus, 7 = truck

    # Crtanje detekcija na slici
    annotated_frame = results[0].plot()

    #cv2.imshow("Detekcija vozila", annotated_frame)
    scale = 0.3  # 0.5 = 50%, 0.3 = 30%, 1.0 = original

    small_frame = cv2.resize(annotated_frame, None, fx=scale, fy=scale)


    if frame_id % skip == 0: # skipuj svaki 180ti frame
        cv2.imshow("Video", small_frame)
        save_id += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    frame_id += 1
    

cap.release()
cv2.destroyAllWindows()