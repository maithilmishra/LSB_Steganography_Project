# backend/decode.py
import cv2
import numpy as np
from .utils import binary_to_message

def extract_data(stego_image_path: str) -> str:
    """
    Extract hidden message from a stego image.
    Works with PNG, BMP, JPG, and JPEG.
    """
    image = cv2.imread(stego_image_path)
    if image is None:
        raise FileNotFoundError("Stego image not found or invalid format.")
    if image.dtype != np.uint8:
        image = image.astype(np.uint8)

    binary_data = ""
    h, w, _ = image.shape

    for row in range(h):
        for col in range(w):
            pixel = image[row, col]
            for ch in range(3):  # B, G, R
                lsb = int(pixel[ch]) & 1
                binary_data += str(lsb)

    message = binary_to_message(binary_data)
    return message
