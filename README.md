# Helmet Detection and License Plate Recognition with Email Notification

## Project Overview
This project is an AI-powered system designed to detect whether a rider is wearing a helmet while riding a two-wheeler. If the rider is not wearing a helmet, the system captures the driver's image, detects their license plate, and sends an automated email notification to the registered owner of the vehicle. This solution leverages deep learning models for object detection and Optical Character Recognition (OCR) for license plate recognition.

## Features
- **Helmet Detection**: Identifies whether a rider is wearing a helmet using a YOLOv8-based object detection model.
- **Driver Image Cropping**: If no helmet is detected, the rider's face is cropped and saved.
- **License Plate Detection and OCR**: Detects the vehicle’s license plate and extracts text using EasyOCR.
- **Automated Email Notification**: Sends an email alert to the registered owner, including the captured image as an attachment.

## Technologies Used
- **YOLOv8** (Ultralytics) for object detection
- **OpenCV** for image processing
- **EasyOCR** for Optical Character Recognition (OCR)
- **SMTP (smtplib)** for sending emails
- **Python** for scripting

## Project Workflow
### 1. Helmet Detection
- Load the trained YOLO model for helmet detection.
- Process the input image and detect whether a helmet is present.
- If a helmet is detected, no further action is taken.
- If a helmet is not detected, the rider’s face is cropped and saved.

### 2. License Plate Detection and OCR
- Load the trained YOLO model for license plate detection.
- Detect and crop the license plate from the saved rider’s image.
- Convert the cropped plate image to grayscale and apply thresholding.
- Extract the license plate text using EasyOCR.

### 3. Email Notification
- If a license plate is detected, an email is automatically sent to the registered owner.
- The email contains a warning message and the cropped image of the rider without a helmet.

## Prerequisites
### Install Dependencies
Ensure you have Python installed and run the following command to install the required libraries:
```bash
pip install ultralytics opencv-python easyocr smtplib numpy
```

## Project Directory Structure
```
Helmet-Detection-Project/
│── models/
│   ├── helmet_model.pt  # Trained YOLO model for helmet detection
│   ├── plate_model.pt   # Trained YOLO model for license plate detection
│── images/
│   ├── no_helmet.jpg    # Sample input image
│── scripts/
│   ├── detect_helmet.py # Helmet detection script
│   ├── detect_plate.py  # License plate detection script
│   ├── send_email.py    # Email notification script
│── main.py              # Integrates all functionalities
│── README.md
```

## Usage
### Running the Project
1. Place the trained YOLO models inside the `models/` folder.
2. Place the test images in the `images/` directory.
3. Update the email credentials in the `main.py` file.
4. Run the main script:
   ```bash
   python main.py
   ```
5. If a violation is detected, the system will send an email to the corresponding vehicle owner.

## Future Enhancements
- Deploy as a real-time video-based system using CCTV feeds.
- Improve OCR accuracy with additional pre-processing techniques.
- Integrate a database to store violation records.



