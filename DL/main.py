from ultralytics import YOLO
import cv2
import os
import easyocr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Define paths for models and input images
helmet_model_path = r"C:\Users\91964\OneDrive\Desktop\DL\runs\detect\train20\weights\best.pt"
plate_model_path = r"C:\Users\91964\OneDrive\Desktop\DL\runs\detect\train22\weights\best.pt"
input_image_path = r"C:\Users\91964\OneDrive\Desktop\DL\no_helmet.jpg"
email_address = "ambatijayacharan18@gmail.com"
email_password = "jnzu ewoa orde weyx"

# Step 1: Helmet Detection
def detect_helmet():
    model = YOLO(helmet_model_path)
    image = cv2.imread(input_image_path)
    results = model.predict(image)
    helmet_detected = False
    driver_box = None

    for detection in results[0].boxes:
        if detection.cls == 0:  # Assuming '0' is the helmet class index
            helmet_detected = True
        elif detection.cls == 1:  # Assuming '1' is the driver class index
            driver_box = detection.xyxy[0]

    if not helmet_detected and driver_box is not None:
        x1, y1, x2, y2 = map(int, driver_box)
        cropped_driver = image[y1:y2, x1:x2]
        no_helmet_path = r"C:\Users\91964\OneDrive\Desktop\DL\no_helmet_detected"
        os.makedirs(no_helmet_path, exist_ok=True)
        output_image_path = os.path.join(no_helmet_path, "no_helmet_" + os.path.basename(input_image_path))
        cv2.imwrite(output_image_path, cropped_driver)
        print(f"Cropped driver image saved at {output_image_path}")
        return output_image_path
    return None

# Step 2: License Plate Detection and OCR
def detect_license_plate(driver_image_path):
    model = YOLO(plate_model_path)
    reader = easyocr.Reader(['en'])
    image = cv2.imread(driver_image_path)
    results = model(image)

    plate_text = ""
    if results and results[0].boxes is not None:
        for i, box in enumerate(results[0].boxes):
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cropped_plate = image[y1:y2, x1:x2]
            gray_plate = cv2.cvtColor(cropped_plate, cv2.COLOR_BGR2GRAY)
            _, threshold_plate = cv2.threshold(gray_plate, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            text_results = reader.readtext(threshold_plate)
            for text in text_results:
                plate_text += text[1] + " "
    print("Detected License Plate Text:", plate_text.strip())
    return plate_text.strip()

# Step 3: Send Email Notification with Image Attachment
def send_email(image_path):
    try:
        # Set up the email server and log in
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_address, email_password)

        # Create email message
        msg = MIMEMultipart()
        msg['From'] = 'ambatijayacharan18@gmail.com'
        msg['To'] = '99220040237@klu.ac.in'
        msg['Subject'] = "Helmet Reminder"

        # Email body without license plate text
        body = (
            "Dear Rider,\n\n"
            "Our system detected you without a helmet.\n\n"
            "Please wear a helmet for your safety.\n\n"
            "Stay Safe!"
        )
        msg.attach(MIMEText(body, 'plain'))

        # Attach the image
        with open(image_path, 'rb') as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(image_path))
            msg.attach(img)

        # Send the email
        server.send_message(msg)
        print('Mail sent successfully with image attachment.')
    except Exception as e:
        print(f"An error occurred while sending email: {e}")
    finally:
        server.quit()

# Integrate all steps
driver_image_path = detect_helmet()
if driver_image_path:
    license_plate_text = detect_license_plate(driver_image_path)
    if license_plate_text:
        send_email(driver_image_path)
    else:
        print("License plate could not be detected.")
else:
    print("Helmet detected, no action needed.")
