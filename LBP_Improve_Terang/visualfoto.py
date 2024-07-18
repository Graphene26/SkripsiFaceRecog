import cv2
import numpy as np
import matplotlib.pyplot as plt

def get_lbp_image(image):
    height, width = image.shape
    lbp_image = np.zeros_like(image, dtype=np.uint8)

    for i in range(1, height-1):
        for j in range(1, width-1):
            center = image[i, j]
            binary = (
                (image[i-1, j-1] >= center) << 7 | (image[i-1, j] >= center) << 6 |
                (image[i-1, j+1] >= center) << 5 | (image[i, j+1] >= center) << 4 |
                (image[i+1, j+1] >= center) << 3 | (image[i+1, j] >= center) << 2 |
                (image[i+1, j-1] >= center) << 1 | (image[i, j-1] >= center) << 0
            )
            lbp_image[i-1, j-1] = binary
    return lbp_image

def histogram_lbp(lbp_image, num_points, radius):
    bins = num_points * (num_points - 1) + 3
    hist, _ = np.histogram(lbp_image.ravel(), bins=np.arange(257), density=True)
    return hist

# Load a grayscale image
image_path = 'X:\\Skripsi\\Progress\\SkripsiFaceRecog\\LBP_Improve_Terang\\Dataset\\Gray.User.1.5.jpg'  # Adjust the path to your image file
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
image = cv2.resize(image, (240, 240))  # Resize image to 240x240 if not already

# Calculate LBP
lbp_image = get_lbp_image(image)

# Calculate Histogram from LBP
radius = 1
num_points = 8 * radius
hist = histogram_lbp(lbp_image, num_points, radius)

# Visualize and save the histogram
plt.figure(figsize=(10, 4))
plt.bar(np.arange(256), hist, width=0.8, color='black')
plt.title('LBP Histogram')
plt.xlabel('LBP Value')
plt.ylabel('Frequency')
plt.ylim(0, 0.07)  # Set y-axis limits to [0, 0.10]
plt.grid(True)

# Save the plot
output_path = r'X:\\Skripsi\\Progress\\SkripsiFaceRecog\\LBP_Improve_Terang\\Visualisasi\\lbp_histogram15.png'
plt.savefig(output_path)
plt.close()  # Close the figure to free memory

print(f"Histogram saved to {output_path}")
