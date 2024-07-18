import os
import sys
from PIL import Image
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
import time

base_dir = r'LBP_Improve_Terang'
input_folder = os.path.join(base_dir, 'Dataset')
decimal_output_folder = os.path.join(base_dir, 'Hasil Decimal')
encrypted_output_folder = os.path.join(base_dir, 'Dataset')
os.makedirs(decimal_output_folder, exist_ok=True)
os.makedirs(encrypted_output_folder, exist_ok=True)

def process_images_to_decimal(input_folder, output_folder):
    files = [f for f in os.listdir(input_folder) if f.endswith('.jpg')]
    for file_name in files:
        image_path = os.path.join(input_folder, file_name)
        img = Image.open(image_path)
        if img.mode != 'L':
            img = img.convert('L')
        width, height = img.size
        decimal_values = [img.getpixel((x, y)) for y in range(height) for x in range(width)]
        output_file_path = os.path.join(output_folder, f'{file_name[:-4]}.txt')
        with open(output_file_path, 'w') as file:
            file.write(','.join(map(str, decimal_values)))
        print(f"Decimal values for {file_name} have been saved to {output_file_path}")
        os.remove(image_path)  # Delete the original image file after processing

def encrypt_data(data, key):
    iv = os.urandom(16)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return iv, encrypted_data

def save_encrypted_data(iv, encrypted_data, filename):
    base64_encoded_iv = base64.b64encode(iv).decode('utf-8')
    base64_encoded_data = base64.b64encode(encrypted_data).decode('utf-8')
    with open(filename, 'w') as file:
        file.write(base64_encoded_iv + '\n' + base64_encoded_data)
    print(f"Encrypted data saved to {filename}")

def encrypt_text_files_in_folder(folder_path, output_folder, key):
    files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'rb') as file:
            text_data = file.read()
        iv, encrypted_data = encrypt_data(text_data, key)
        encrypted_file_name = f'Encrypt_{file_name}'
        encrypted_file_path = os.path.join(output_folder, encrypted_file_name)
        save_encrypted_data(iv, encrypted_data, encrypted_file_path)
        os.remove(file_path)  # Delete the original decimal file after encrypting

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python 1encrypt.py <encryption_key>")
        sys.exit(1)
    
    encryption_key = sys.argv[1].encode('utf-8')
    if len(encryption_key) != 16:
        print("Invalid key length. Key must be exactly 16 characters long.")
        sys.exit(1)

    process_images_to_decimal(input_folder, decimal_output_folder)
    encrypt_text_files_in_folder(decimal_output_folder, encrypted_output_folder, encryption_key)
