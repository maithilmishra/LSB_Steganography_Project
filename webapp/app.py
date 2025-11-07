# webapp/app.py
from flask import Flask, render_template, request
import os, base64, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import cv2
from PIL import Image
from backend.encode import hide_data
from backend.decode import extract_data
from backend.crypto_utils import (
    generate_session_keys, aes_gcm_encrypt, aes_gcm_decrypt,
    rsa_wrap_keys, rsa_unwrap_keys
)
from backend.analysis import analyze_images

app = Flask(__name__)
UPLOAD_FOLDER, OUTPUT_FOLDER = 'input', 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/embed', methods=['POST'])
def embed():
    file = request.files['cover_image']
    message = request.form['message']
    pubkey_file = request.files.get('receiver_pubkey')

    if not pubkey_file:
        return "❌ Receiver public key file required."

    receiver_pub = pubkey_file.read().decode('utf-8')

    if file:
        filename = file.filename
        ext = filename.lower().split('.')[-1]

        # convert JPG/JPEG to PNG automatically
        if ext in ['jpg', 'jpeg']:
            from PIL import Image
            img = Image.open(file.stream).convert("RGB")
            filename = filename.rsplit('.', 1)[0] + ".png"
            cover_path = os.path.join(UPLOAD_FOLDER, filename)
            img.save(cover_path, "PNG")
        else:
            cover_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(cover_path)

        import cv2
        img = cv2.imread(cover_path)
        h, w, _ = img.shape
        max_chars = (h * w * 3) // 8
        if len(message) > max_chars:
            return f"❌ Message too long! Max {max_chars} characters."

        # Generate AES + randomization keys
        from backend.crypto_utils import generate_session_keys, aes_gcm_encrypt, rsa_wrap_keys
        aes_key, rand_key = generate_session_keys()

        # Encrypt message
        cipher_blob = aes_gcm_encrypt(message, aes_key)

        # Embed ciphertext into image
        from backend.encode import hide_data
        success = hide_data(cover_path, os.path.join(OUTPUT_FOLDER, f"stego_{filename}"), cipher_blob, rand_key)
        if not success:
            return "Embedding failed."

        # Wrap AES and random keys with receiver public key
        wrapped_b64 = rsa_wrap_keys(aes_key, rand_key, receiver_pub)

        stego_filename = f"stego_{filename}"
        return render_template('result.html',
                            stego_image=stego_filename,
                            wrapped=wrapped_b64)

    return "No file uploaded."

@app.route('/extract', methods=['POST'])
def extract():
    file = request.files['stego_image']
    privkey_file = request.files.get('receiver_privkey')
    wrapped_b64 = request.form.get('wrapped_blob', '').strip()

    if not (file and privkey_file and wrapped_b64):
        return "❌ Stego image, private key, and wrapped blob required."

    receiver_priv = privkey_file.read().decode('utf-8')

    stego_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(stego_path)

    from backend.crypto_utils import rsa_unwrap_keys, aes_gcm_decrypt
    from backend.decode import extract_data

    aes_key, rand_key = rsa_unwrap_keys(wrapped_b64, receiver_priv)
    cipher_blob = extract_data(stego_path, rand_key)

    try:
        message = aes_gcm_decrypt(cipher_blob, aes_key)
    except Exception:
        message = "❌ Decryption failed or corrupted data."

    return render_template('extracted.html', message=message)

@app.route('/analyze', methods=['POST'])
def analyze():
    cover, stego = request.files['cover_image'], request.files['stego_image']
    if cover and stego:
        cpath, spath = os.path.join(UPLOAD_FOLDER, cover.filename), os.path.join(UPLOAD_FOLDER, stego.filename)
        cover.save(cpath); stego.save(spath)
        mse, psnr, hist = analyze_images(cpath, spath)
        return render_template('analysis.html', mse=mse, psnr=psnr, hist_datauri=hist)
    return "Upload both images."

from flask import send_from_directory

@app.route('/output/<path:filename>')
def download_file(filename):
    """Allow viewing/downloading stego images."""
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=False)


if __name__ == '__main__':
    app.run(debug=True)
