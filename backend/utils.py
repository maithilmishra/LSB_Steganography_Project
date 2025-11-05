# backend/utils.py
DELIMITER = "#####"

def message_to_binary(message: str) -> str:
    """Convert message to a binary string."""
    return ''.join(format(ord(ch), '08b') for ch in message)

def binary_to_message(binary_data: str) -> str:
    """Convert binary string back to readable text."""
    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded = ""
    for byte in all_bytes:
        decoded += chr(int(byte, 2))
        if decoded.endswith(DELIMITER):
            break
    return decoded.replace(DELIMITER, '')
