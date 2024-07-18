import os

# Tentukan direktori tempat file berada
directory = r'X:\Skripsi\Progress\SkripsiFaceRecog\LBP_Improve_Terang\Dataset'

# Loop melalui semua file dalam direktori
for filename in os.listdir(directory):
    if filename.startswith("Gray."):
        # Membangun jalur penuh file lama dan baru
        old_file_path = os.path.join(directory, filename)
        new_filename = filename.replace("Gray.", "")  # Menghapus "Gray." dari nama file
        new_file_path = os.path.join(directory, new_filename)
        
        # Ganti nama file
        try:
            os.rename(old_file_path, new_file_path)
            print(f"Renamed '{filename}' to '{new_filename}'")
        except Exception as e:
            print(f"Error renaming '{filename}': {e}")

print("Renaming process is completed.")
