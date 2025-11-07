# backend/encode.py
import cv2, numpy as np, random, hashlib
from backend.utils import message_to_binary, DELIMITER

def hide_data(image_path, output_path, message, key=""):
    image = cv2.imread(image_path)
    if image is None:
        return False

    h, w, _ = image.shape
    total_pixels = h * w
    binary_message = message_to_binary(message + DELIMITER)
    if len(binary_message) > total_pixels * 3:
        return False

    indices = list(range(total_pixels))
    if key:
        seed = int(hashlib.sha256(key.encode()).hexdigest(), 16) % (10**8)
        random.seed(seed)
        random.shuffle(indices)

    flat = image.reshape(-1, 3)
    data_i = 0
    for idx in indices:
        for ch in range(3):
            if data_i < len(binary_message):
                flat[idx][ch] = (flat[idx][ch] & ~1) | int(binary_message[data_i])
                data_i += 1
        if data_i >= len(binary_message): break

    cv2.imwrite(output_path, flat.reshape(image.shape))
    return True
