import cv2
import numpy as np
import os
import csv
import time
import serial  # Import serial to handle serial communication

# Define base directory
base_dir = r"LBP_Improve_Terang"

# Setup Camera
camera = 0
video = cv2.VideoCapture(camera, cv2.CAP_DSHOW)

# Face Recognition Setup
cascade_path = os.path.join(base_dir, 'Model', 'lbpcascade_frontalface_improved.xml')
model_path = os.path.join(base_dir, 'Dataset', 'lbp_terang4.xml')

faceDeteksi = cv2.CascadeClassifier(cascade_path)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(model_path)

# Serial setup
ser = serial.Serial('COM9', 115200, timeout=1)  # Adjust the COM port and baud rate

# Load user names from CSV
id_to_name = {}
csv_file = os.path.join(base_dir, 'database.csv')
with open(csv_file, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        id_to_name[int(row['ID'])] = row['Nama']

# Initialize counters for accuracy calculation
correct_predictions = 0
total_predictions = 0
start_time = time.time()
session_active = True
warmup_time = 10  # 10 seconds warm-up before starting detection

while session_active:
    _, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceDeteksi.detectMultiScale(gray, 1.3, 5)
    face_detected = False

    current_time = time.time()
    if current_time - start_time > warmup_time:  # Only start detecting after warm-up
        for (x, y, w, h) in faces:
            id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            total_predictions += 1
            face_detected = True

            # Display the box and ID only for registered faces
            name = id_to_name.get(id, "Unknown")  # Fetch name if ID is recognized, otherwise 'Unknown'
            if conf <= 80:
                correct_predictions += 1
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"{name} (ID: {id})", (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow("Face Recognition", frame)

    # Calculate and display accuracy only when faces are detected and after warm-up
    if face_detected and current_time - start_time > warmup_time:
        if total_predictions > 0:
            accuracy = (correct_predictions / total_predictions) * 100
            print(f"Accuracy: {accuracy:.2f}%")
            # Send unlock command if accuracy is above 90%
            if accuracy > 90:
                ser.write(b'UNLOCK\n')
            correct_predictions = 0
            total_predictions = 0
        start_time = current_time  # Reset timer

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
