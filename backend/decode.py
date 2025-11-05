# backend/decode.py
import cv2
from .utils import binary_to_message, DELIMITER

def extract_data(stego_image_path: str) -> str:
    image = cv2.imread(stego_image_path)
    if image is None:
        raise FileNotFoundError("Stego image not found or invalid format.")
    h, w, _ = image.shape
    binary_data = ''

    for row in range(h):
        for col in range(w):
            pixel = image[row, col]
            for ch in range(3):
                binary_data += str(int(pixel[ch]) & 1)
    # decode to text until delimiter
    message = binary_to_message(binary_data)
    return message
