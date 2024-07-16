import sys
import cv2
import csv
import os

def check_duplicate(id, nama, csv_file):
    """Check if ID or name already exists in the CSV file."""
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['ID'] == id or row['Nama'] == nama:
                    print(f"ID {id} or Name {nama} already exists in the database.")
                    return True
    except FileNotFoundError:
        print("CSV file not found.")
        return False
    return False

if len(sys.argv) != 3:
    print("Usage: python rekam.py <ID> <Nama>")
    sys.exit(1)

id, nama = sys.argv[1], sys.argv[2]
base_dir = r"D:\Skripsi\Code Progress\Final Code\LBP_Improve_Terang"  # Use raw string
csv_file = os.path.join(base_dir, 'database.csv')
image_dir = base_dir

if not os.path.exists(image_dir):
    os.makedirs(image_dir)

if check_duplicate(id, nama, csv_file):
    sys.exit(1)

camera = 0
video = cv2.VideoCapture(camera, cv2.CAP_DSHOW)
faceDeteksi = cv2.CascadeClassifier(os.path.join(base_dir, "lbpcascade_frontalface_improved.xml"))

fieldnames = ['ID', 'Nama']
try:
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow({'ID': id, 'Nama': nama})
except IOError:
    print("Failed to open or write to CSV file")

a = 0
while True:
    a += 1
    _, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceDeteksi.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cropped_face = gray[y:y+h, x:x+w]
        resized_face = cv2.resize(cropped_face, (240, 240))
        cv2.imwrite(os.path.join(image_dir, f'User.{id}.{a}.jpg'), resized_face)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow("Face Recognition Window", frame)
    if cv2.waitKey(500) == ord('q') or a > 49:
        print("Recording completed.")
        break

video.release()
cv2.destroyAllWindows()
