import tkinter as tk
from tkinter import simpledialog, messagebox
import subprocess
import csv
import os
import serial

# Define base directory and file locations
# Lokasi database dan folder penyimpanan gambar
base_dir = "D:\\Skripsi\\Code Progress\\Final Code\\LBP_Improve_Terang"


csv_file = os.path.join(base_dir, 'database.csv')

# Adjust this to match your ESP32 serial port
serial_port = 'COM9'
baud_rate = 115200

def check_duplicate(id, name, csv_file):
    """Check if the ID or name already exists in the CSV file."""
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['ID'] == id or row['Nama'] == name:
                    return f"ID {id} or Name {name} already exists in the database."
    except FileNotFoundError:
        return "File not found."
    return None

def run_script(script_name, id=None, name=None):
    """Function to run a separate Python script and handle outputs."""
    args = ['python', os.path.join(base_dir, script_name)]
    if id and name:
        args.extend([id, name])
    result = subprocess.run(args, capture_output=True, text=True)
    if result.stdout:
        print("Script Output:", result.stdout)
    if result.stderr:
        print("Script Error:", result.stderr)

def ask_user_details():
    """Function to request ID and name from the user."""
    id = simpledialog.askstring("Input", "Enter ID:", parent=root)
    name = simpledialog.askstring("Input", "Enter Name:", parent=root)
    if id and name:
        duplicate_message = check_duplicate(id, name, csv_file)
        if not duplicate_message:
            run_script('rekam.py', id, name)
        else:
            messagebox.showwarning("Duplicate", duplicate_message)

def create_app(window):
    """Create the GUI layout with buttons to execute scripts."""
    window.title('Neuro Smart Door Lock')
    window.geometry('750x480')
    window.config(bg='#1a1a2e')

    label_info = tk.Label(window, text="Register Face Recognition", font=('Helvetica', 16), bg='#1a1a2e', fg='#e94560')
    label_info.pack(pady=(10, 20))

    btn_font = ('Helvetica', 12)
    btn_padding = {'padx': 10, 'pady': 5}

    btn_rekam = tk.Button(window, text="Record", command=ask_user_details, bg='#0f3460', fg='#e94560', font=btn_font, **btn_padding)
    btn_rekam.pack(pady=10)

    btn_training = tk.Button(window, text="Training", command=lambda: run_script('training.py'), bg='#0f3460', fg='#e94560', font=btn_font, **btn_padding)
    btn_training.pack(pady=10)

    btn_scan = tk.Button(window, text="Scan", command=lambda: run_script('scan.py'), bg='#0f3460', fg='#e94560', font=btn_font, **btn_padding)
    btn_scan.pack(pady=(10, 40))

    label_action = tk.Label(window, text="Secure Your Dataset", font=('Helvetica', 14), bg='#1a1a2e', fg='#e94560')
    label_action.pack(pady=(10, 10))

    btn_encrypt = tk.Button(window, text="Encrypt", command=lambda: run_script('encrypt_dataset.py'), bg='#0f3460', fg='#e94560', font=btn_font, **btn_padding)
    btn_encrypt.pack(pady=10)

    btn_decrypt = tk.Button(window, text="Decrypt", command=lambda: run_script('decrypt.py'), bg='#0f3460', fg='#e94560', font=btn_font, **btn_padding)
    btn_decrypt.pack(pady=10)

if __name__ == '__main__':
    root = tk.Tk()
    create_app(root)
    root.mainloop()
