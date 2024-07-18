import os
from PIL import Image
import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64

# Base directory and subdirectories for input and output
base_dir = r'LBP_Improve_Terang'
encrypted_folder = os.path.join(base_dir, 'Dataset')  # Folder containing encrypted files
decimal_output_folder = os.path.join(base_dir, 'Hasil Decimal')  # Folder for decrypted text files
output_folder = os.path.join(base_dir, 'Hasil Decrypt')  # Folder for final images
os.makedirs(decimal_output_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

def read_encrypted_data(file_path):
    """Reads encrypted data from a file, assuming the IV and data are stored in base64 format."""
    with open(file_path, 'r') as file:
        base64_encoded_iv = file.readline().strip()
        base64_encoded_data = file.readline().strip()
    iv = base64.b64decode(base64_encoded_iv)
    encrypted_data = base64.b64decode(base64_encoded_data)
    return iv, encrypted_data

def decrypt_data(encrypted_data, key, iv):
    """Decrypts data using AES CBC mode."""
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    print("Data has been successfully decrypted.")
    return data

def create_image_from_decimal(input_file_path, output_image_path, image_size=(240, 240)):
    """Converts decimal data back to an image and saves it."""
    with open(input_file_path, 'r') as file:
        decimal_values = file.read().split(',')
    data_array = np.array(list(map(int, decimal_values)), dtype=np.uint8).reshape(image_size)
    new_image = Image.fromarray(data_array, 'L')
    new_image.save(output_image_path)
    print(f"Image has been recreated from decimal data and saved to {output_image_path}")

def process_files(encrypted_folder, decimal_output_folder, output_folder, key):
    """Decrypts files and converts them back to images."""
    files = [f for f in os.listdir(encrypted_folder) if f.startswith('Encrypt_') and f.endswith('.txt')]
    for file_name in files:
        encrypted_file_path = os.path.join(encrypted_folder, file_name)
        iv, encrypted_data = read_encrypted_data(encrypted_file_path)
        decrypted_data = decrypt_data(encrypted_data, key, iv)
        print(f"Data decrypted for {file_name}")
        decrypted_file_name = file_name[len('Encrypt_'):]
        decrypted_file_path = os.path.join(decimal_output_folder, decrypted_file_name)
        with open(decrypted_file_path, 'w') as file:
            file.write(decrypted_data.decode('utf-8'))
        output_image_path = os.path.join(output_folder, decrypted_file_name.replace('.txt', '.jpg'))
        create_image_from_decimal(decrypted_file_path, output_image_path)
        os.remove(decrypted_file_path)  # Optionally remove the intermediate decimal file
        print(f"Decrypted data saved to {decrypted_file_path} and intermediate file removed.")

def get_valid_key():
    """Prompts for a valid 16-character AES encryption key."""
    key_input = input("Enter an encryption key (exactly 16 characters): ")
    while len(key_input) != 16:
        key_input = input("Invalid key length. Key must be exactly 16 characters long: ")
    return key_input.encode('utf-8')

if __name__ == "__main__":
    key = get_valid_key()
    process_files(encrypted_folder, decimal_output_folder, output_folder, key)
