# backend/utils.py
from typing import List

DELIMITER = "#####"

def message_to_binary(message: str) -> str:
    """Convert string message to binary string of 8-bit bytes."""
    return ''.join([format(ord(ch), '08b') for ch in message])

def binary_to_message(binary_data: str) -> str:
    """Convert binary string back to text, stop when delimiter reached."""
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    text = ''
    for byte in chars:
        if len(byte) < 8:
            break
        text += chr(int(byte, 2))
        if text.endswith(DELIMITER):
            return text[:-len(DELIMITER)]
    return text
