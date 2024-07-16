import json
from matplotlib import pyplot as plt
import numpy as np

# Memuat data histogram dari file JSON
with open('histograms.json', 'r') as file:
    data = json.load(file)

# Ambil histogram untuk label tertentu, misalnya label '1'
histogram = np.array(data['1'])  # Pastikan labelnya sesuai dengan yang Anda simpan

# Sekarang plot histogram tersebut
plt.figure(figsize=(10, 5))
plt.bar(range(len(histogram)), histogram, color='blue')
plt.title('Visualisasi Histogram')
plt.xlabel('Index Bins')
plt.ylabel('Frekuensi')
plt.grid(True)
plt.savefig('histogram.png')
plt.show()
