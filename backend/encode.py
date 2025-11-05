# backend/encode.py
import cv2
import numpy as np
from .utils import message_to_binary, DELIMITER

def can_store(image: np.ndarray, message: str) -> bool:
    """Check capacity: 3 bits per pixel (RGB)."""
    h, w, _ = image.shape
    capacity_bits = h * w * 3
    required_bits = (len(message) + len(DELIMITER)) * 8
    return required_bits <= capacity_bits

def hide_data(cover_image_path: str, output_path: str, secret_message: str) -> bool:
    """Embed secret_message into image and save to output_path. Returns True on success."""
    image = cv2.imread(cover_image_path)
    if image is None:
        raise FileNotFoundError("Cover image not found or invalid format.")
    if image.dtype != np.uint8:
        image = image.astype(np.uint8)

    message = secret_message + DELIMITER
    binary_message = message_to_binary(message)
    data_len = len(binary_message)
    h, w, _ = image.shape
    total_pixels = h * w

    if not can_store(image, secret_message):
        return False

    data_index = 0
    # iterate over pixels
    for row in range(h):
        for col in range(w):
            pixel = image[row, col]
            r, g, b = pixel[0], pixel[1], pixel[2]  # OpenCV BGR order but we treat as channels
            channels = [int(r), int(g), int(b)]
            for ch in range(3):
                if data_index < data_len:
                    channels[ch] = (channels[ch] & 0b11111110) | int(binary_message[data_index])
                    channels[ch] = np.uint8(channels[ch])  # ensure within uint8 range
                    data_index += 1
            image[row, col] = channels
            if data_index >= data_len:
                break
        if data_index >= data_len:
            break

    cv2.imwrite(output_path, image)
    return True
