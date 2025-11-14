import cv2
import os

video_path = "magla1.mp4"
output_folder = "frames"
os.makedirs(output_folder, exist_ok=True)

cap = cv2.VideoCapture(video_path)
frame_id = 0
save_id = 0

skip = 180

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if frame_id % skip == 0: # skipuj svaki 180ti frame
        cv2.imwrite(f"{output_folder}/frame{save_id:04d}.jpg", frame)
        save_id += 1

    frame_id += 1

cap.release()