import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox, QInputDialog
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess
import csv
import os

base_dir = r'LBP_Improve_Terang'
csv_file = os.path.join(base_dir, 'database.csv')

class EncryptionThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, script_name, encryption_key=None):
        super().__init__()
        self.script_name = script_name
        self.encryption_key = encryption_key

    def run(self):
        args = ['python', os.path.join(base_dir, self.script_name), self.encryption_key]
        try:
            result = subprocess.run(args, capture_output=True, text=True, check=True)
            self.finished.emit(self.script_name + ": " + result.stdout)  # Include script name in the message
        except subprocess.CalledProcessError as e:
            self.finished.emit(self.script_name + ": Error - " + e.stderr)  # Include script name in the error message


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.active_threads = []  # Keep track of active threads

    def initUI(self):
        self.setWindowTitle('Neuro Smart Door Lock')
        self.setGeometry(300, 300, 750, 480)
        layout = QVBoxLayout()

        self.label_info = QLabel("Register Face Recognition")
        layout.addWidget(self.label_info)

        self.btn_rekam = QPushButton("Record")
        self.btn_rekam.clicked.connect(self.ask_user_details)
        layout.addWidget(self.btn_rekam)

        self.btn_encrypt = QPushButton("Encrypt Dataset")
        self.btn_encrypt.clicked.connect(self.request_encryption_key)
        layout.addWidget(self.btn_encrypt)

        self.btn_decrypt = QPushButton("Decrypt Dataset")
        self.btn_decrypt.clicked.connect(self.request_decryption_key)
        layout.addWidget(self.btn_decrypt)

        self.btn_training = QPushButton("Training")
        self.btn_training.clicked.connect(lambda: self.run_script('training.py'))
        layout.addWidget(self.btn_training)

        self.btn_scan = QPushButton("Scan")
        self.btn_scan.clicked.connect(lambda: self.run_script('scan.py'))
        layout.addWidget(self.btn_scan)

        self.setLayout(layout)

    def request_encryption_key(self):
        key, okPressed = QInputDialog.getText(self, "Enter Encryption Key", "Enter an encryption key (exactly 16 characters):", QLineEdit.Normal, "")
        if okPressed and len(key) == 16:
            self.run_encryption_script('1encrypt.py', encryption_key=key)
        elif okPressed:
            QMessageBox.warning(self, "Invalid Key", "The key must be exactly 16 characters long.")

    def request_decryption_key(self):
        key, okPressed = QInputDialog.getText(self, "Enter Decryption Key", "Enter the decryption key (exactly 16 characters):", QLineEdit.Normal, "")
        if okPressed and len(key) == 16:
            self.run_encryption_script('decrypt.py', encryption_key=key)
        elif okPressed:
            QMessageBox.warning(self, "Invalid Key", "The key must be exactly 16 characters long.")

    def run_encryption_script(self, script_name, encryption_key):
        thread = EncryptionThread(script_name, encryption_key=encryption_key)
        thread.finished.connect(self.show_message)
        thread.start()
        self.active_threads.append(thread)

    def run_script(self, script_name, id=None, name=None):
        args = ['python', os.path.join(base_dir, script_name)]
        if id and name:
            args.extend([id, name])
        try:
            result = subprocess.run(args, capture_output=True, text=True, check=True)
            QMessageBox.information(self, "Script Output", result.stdout)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Script Error", e.stderr)

    def show_message(self, message):
        if 'decrypt.py' in message:
            QMessageBox.information(self, "Script Output", "File telah terdekripsi")
        else:
            QMessageBox.information(self, "Script Output", message)
        self.cleanup_threads()



    def cleanup_threads(self):
        self.active_threads = [t for t in self.active_threads if t.isRunning()]

    def ask_user_details(self):
        id, okPressed = QInputDialog.getText(self, "Input", "Enter ID:", QLineEdit.Normal, "")
        name, okPressed = QInputDialog.getText(self, "Input", "Enter Name:", QLineEdit.Normal, "")
        if okPressed and id and name:
            message = self.check_duplicate(id, name)
            if not message:
                self.run_script('rekam.py', id=id, name=name)
            else:
                QMessageBox.warning(self, "Duplicate", message)

    def check_duplicate(self, id, name):
        try:
            with open(csv_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['ID'] == id or row['Nama'] == name:
                        return f"ID {id} or Name {name} already exists in the database."
        except FileNotFoundError:
            return "File not found."
        return None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
