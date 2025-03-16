import cv2
import torch
from ultralytics import YOLO
import os

# Load YOLO model for helmet detection
helmet_model = YOLO(r"C:\Users\91964\OneDrive\Desktop\DL\runs\detect\train6\weights\best.pt")

# Load the Haar cascade for number plate detection
plate_cascade = cv2.CascadeClassifier("model/haarcascade_russian_plate_number.xml")

# Ensure the 'plates' directory exists
output_folder = "plates"
os.makedirs(output_folder, exist_ok=True)

# Open the video file (using a raw string to handle the path correctly)
cap = cv2.VideoCapture(r"C:\Users\91964\OneDrive\Desktop\DL\he2.mp4")
min_area = 500
count = 0

while cap.isOpened():
    success, img = cap.read()
    if not success:
        break

    # Convert image to RGB format for YOLO model
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Run YOLO model for helmet detection
    results = helmet_model.predict(img_rgb)
    helmet_detected = False

    # Parse YOLO detections
    for result in results:
        if len(result.boxes) > 0:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = box.conf[0]
                label = box.cls[0]

                # Check if the detected object is a helmet (adjust label if needed)
                if label == 0 and confidence > 0.5:  # Assuming class 0 is 'helmet'
                    helmet_detected = True
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(img, "Helmet", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # If no helmet is detected, proceed with license plate detection
    if not helmet_detected:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

        for (px, py, pw, ph) in plates:
            area = pw * ph
            if area > min_area:
                cv2.rectangle(img, (px, py), (px + pw, py + ph), (0, 0, 255), 2)
                img_roi = img[py: py + ph, px: px + pw]
                cv2.putText(img, "Number Plate", (px, py - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.imshow("Number Plate", img_roi)

                # Save the plate image
                plate_filename = os.path.join(output_folder, f"plate_{count}.jpg")
                cv2.imwrite(plate_filename, img_roi)
                print(f"Number plate saved to {plate_filename}")
                count += 1

    cv2.imshow("Result", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
