import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt

# Lokasi file XML
file_path = r"X:\Skripsi\Progress\SkripsiFaceRecog\LBP_Improve_Terang\Dataset\lbp_terang1gelap.xml"

# Fungsi untuk memuat histogram dari file XML
def load_histogram_from_xml(file_path):
    # Parse XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Dapatkan data histogram dari elemen <data>
    # Anda mungkin perlu menyesuaikan jalur ini berdasarkan struktur XML yang tepat
    data_element = root.find(".//data")
    histogram_data = data_element.text.strip().split()
    histogram = np.array([float(num) for num in histogram_data])
    
    return histogram

# Memuat histogram
histogram = load_histogram_from_xml(file_path)

# Visualisasi Histogram
plt.figure(figsize=(10, 4))
plt.bar(range(len(histogram)), histogram, color='black')
plt.title('LBP Histogram Visualization')
plt.xlabel('LBP Value Index')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
