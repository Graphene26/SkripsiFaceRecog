import cv2
import numpy as np
import os
import csv
import time

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

# Load user names from CSV
id_to_name = {}
csv_file = os.path.join(base_dir, 'database.csv')
with open(csv_file, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        id_to_name[int(row['ID'])] = row['Nama']

# Initialize counters for accuracy and precision/recall calculation
correct_predictions = 0
total_predictions = 0
true_positives = 0
false_positives = 0
false_negatives = 0

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
        detected_ids = set()
        for (x, y, w, h) in faces:
            id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            total_predictions += 1
            face_detected = True

            # Assume true identity is known for each face (you need a mechanism to get this)
            true_id = id  # This should be obtained from your environment or test setup

            if conf <= 80:
                detected_ids.add(id)
                if id == true_id:
                    true_positives += 1
                else:
                    false_positives += 1
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"{id_to_name.get(id, 'Unknown')} (ID: {id})", (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

        # Update false negatives
        for true_id in id_to_name.keys():
            if true_id not in detected_ids:
                false_negatives += 1

    # Display the resulting frame
    cv2.imshow("Face Recognition", frame)

    # Calculate and display accuracy only when faces are detected and after warm-up
    if face_detected and current_time - start_time > warmup_time:
        if total_predictions > 0:
            accuracy = (correct_predictions / total_predictions) * 100
            precision = true_positives / (true_positives + false_positives) if true_positives + false_positives > 0 else 0
            recall = true_positives / (true_positives + false_negatives) if true_positives + false_negatives > 0 else 0
            print(f"Accuracy: {accuracy:.2f}%, Precision: {precision:.2f}%, Recall: {recall:.2f}%")
            correct_predictions = 0
            total_predictions = 0
        start_time = current_time  # Reset timer

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
