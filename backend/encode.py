# backend/encode.py
import cv2
import numpy as np
from .utils import message_to_binary, DELIMITER

def can_store(image: np.ndarray, message: str) -> bool:
    """Check if image has enough capacity for the message."""
    h, w, _ = image.shape
    capacity_bits = h * w * 3
    required_bits = (len(message) + len(DELIMITER)) * 8
    return required_bits <= capacity_bits

def hide_data(cover_image_path: str, output_path: str, secret_message: str, output_format: str = "PNG") -> bool:
    """
    Embed secret_message into cover_image_path and save to output_path.
    Supported formats: PNG, BMP, JPG, JPEG.
    """
    image = cv2.imread(cover_image_path)
    if image is None:
        raise FileNotFoundError("Cover image not found or invalid format.")
    if image.dtype != np.uint8:
        image = image.astype(np.uint8)

    message = secret_message + DELIMITER
    binary_message = message_to_binary(message)
    data_len = len(binary_message)
    h, w, _ = image.shape

    if not can_store(image, secret_message):
        return False

    data_index = 0
    for row in range(h):
        for col in range(w):
            pixel = image[row, col]
            for ch in range(3):  # B, G, R
                if data_index < data_len:
                    bit = int(binary_message[data_index])
                    pixel[ch] = np.uint8((int(pixel[ch]) & 0b11111110) | bit)
                    data_index += 1
            image[row, col] = pixel
            if data_index >= data_len:
                break
        if data_index >= data_len:
            break

    fmt = (output_format or "PNG").lower()
    if fmt in ("jpg", "jpeg"):
        cv2.imwrite(output_path, image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    else:
        cv2.imwrite(output_path, image)
    return True
