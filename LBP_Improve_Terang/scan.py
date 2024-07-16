import cv2
import numpy as np
import os
import csv

# Define base directory
base_dir = r"LBP_Improve_Terang"

# Setup Camera
camera = 0
video = cv2.VideoCapture(camera, cv2.CAP_DSHOW)

# Face Recognition Setup
cascade_path = os.path.join(base_dir, 'lbpcascade_frontalface_improved.xml')
model_path = os.path.join(base_dir, 'lbp_terang_improved_baru.xml')

faceDeteksi = cv2.CascadeClassifier(cascade_path)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(model_path)

# Load user names from CSV
id_to_name = {}
csv_file = os.path.join(base_dir, 'database.csv')
with open(csv_file, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        id_to_name[int(row['ID'])] = row['Nama']

while True:
    _, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceDeteksi.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        id, conf = recognizer.predict(gray[y:y+h, x:x+w])

        # Modify here to display "Unknown" if confidence is above 45
        if conf > 40:
            name = "Unknown"
        else:
            name = id_to_name.get(id, "Unknown")

        # Print the detected ID, name, and confidence to the console
        print(f"ID: {id}, Name: {name}, Confidence: {conf:.2f}")

        # Visual feedback on the frame
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f"{name} ({conf:.2f})", (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow("Face Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
