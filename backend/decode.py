# backend/decode.py
import cv2, numpy as np, random, hashlib
from backend.utils import binary_to_message

def extract_data(stego_path, key=""):
    image = cv2.imread(stego_path)
    if image is None: return ""
    h, w, _ = image.shape
    total_pixels = h * w
    indices = list(range(total_pixels))
    if key:
        seed = int(hashlib.sha256(key.encode()).hexdigest(), 16) % (10**8)
        random.seed(seed)
        random.shuffle(indices)

    flat = image.reshape(-1, 3)
    bits = ""
    for idx in indices:
        for ch in range(3):
            bits += str(flat[idx][ch] & 1)
    return binary_to_message(bits)
