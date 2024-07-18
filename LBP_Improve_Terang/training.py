import cv2
import os
import numpy as np
from PIL import Image

# Base directory for storing everything
base_dir = r'LBP_Improve_Terang'

# Using LBPHFaceRecognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Using LBP Cascade for face detection
detector = cv2.CascadeClassifier(os.path.join(base_dir, 'Model', 'lbpcascade_frontalface_improved.xml'))

# Function to get images and labels from dataset
def getImagesWithLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))]
    faceSamples = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(imageNp, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            faceSamples.append(imageNp[y:y+h, x:x+w])
            Ids.append(Id)
    return faceSamples, Ids

# Get images and labels from dataset
faces, Ids = getImagesWithLabels(os.path.join(base_dir, 'Hasil Decrypt'))

# Train the face recognizer using the dataset
recognizer.train(faces, np.array(Ids))

# Save the trained face recognition model
recognizer.save(os.path.join(base_dir, 'Dataset', 'lbp.xml'))

# Print a message indicating that training has completed
print("Model Training Telah Selesai")
