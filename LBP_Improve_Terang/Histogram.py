import cv2
import numpy as np
import json
import time
# Misalnya Anda memiliki array `histograms` dan `labels`
histograms = [np.random.rand(256) for _ in range(10)]  # contoh histogram
labels = list(range(10))  # contoh label

# Menyimpan ke JSON
data = {label: histogram.tolist() for label, histogram in zip(labels, histograms)}
with open('histograms.json', 'w') as f:
    json.dump(data, f)

# Memuat dari JSON
with open('histograms.json', 'r') as f:
    loaded_data = json.load(f)
    for label, histogram in loaded_data.items():
        print(f"Label: {label}, Histogram: {np.array(histogram)}")
