import tkinter as tk
from tkinter import simpledialog, messagebox
import subprocess
import serial
import csv
import os
import threading  # Import threading for asynchronous task management

# Define base directory and file locations
base_dir = r'LBP_Improve_Terang'
csv_file = os.path.join(base_dir, 'database.csv')

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
    """Function to run a separate Python script asynchronously and handle outputs."""
    def thread_target():
        args = ['python', os.path.join(base_dir, script_name)]
        if id and name:
            args.extend([id, name])
        result = subprocess.run(args, capture_output=True, text=True)
        if result.stdout:
            print("Script Output:", result.stdout)
        if result.stderr:
            print("Script Error:", result.stderr)
    # Start the script in a new thread to keep the GUI responsive
    threading.Thread(target=thread_target).start()

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

if __name__ == '__main__':
    root = tk.Tk()
    create_app(root)
    root.mainloop()
