from ultralytics import YOLO
import cv2
import cvzone
import math
import time
import random

cap = cv2.VideoCapture(1)  # For Webcam
# cap = cv2.VideoCapture("video.mp4")  # For Video
cap.set(3, 1280)
cap.set(4, 720)

model = YOLO("yolov8l.pt")

classNames = ["person"]

prev_frame_time = 0
new_frame_time = 0

while True:
    new_frame_time = time.time()
    success, img = cap.read()
    if not success:
        break 
    results = model(img, stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1

            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])

            if cls < len(classNames) and classNames[cls] == "person":

                color = (random.randint(0, 127), random.randint(0, 255), random.randint(0, 255))
                
                cvzone.cornerRect(img, (x1, y1, w, h), colorR=color)
                cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1, colorR=color)

    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    print(fps)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
