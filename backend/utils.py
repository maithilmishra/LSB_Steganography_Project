# backend/utils.py
DELIMITER = "#####"

def message_to_binary(message):
    return ''.join(format(ord(c), '08b') for c in message)

def binary_to_message(binary_data):
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message = ''.join(chr(int(b, 2)) for b in chars)
    end_index = message.find(DELIMITER)
    return message[:end_index] if end_index != -1 else message
