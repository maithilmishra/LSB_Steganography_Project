# webapp/app.py
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from backend.encode import hide_data
from backend.decode import extract_data
from backend.analysis import compare_images
from PIL import Image
from base64 import b64encode

# Flask setup
app = Flask(__name__)
app.secret_key = "stegano_secret"
app.config['UPLOAD_FOLDER'] = "../input"
app.config['OUTPUT_FOLDER'] = "../output"
ALLOWED_EXTENSIONS = {'png', 'bmp', 'jpg', 'jpeg'}

# ------------------------------
# Helper functions
# ------------------------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def file_to_datauri(path):
    with open(path, "rb") as f:
        encoded = b64encode(f.read()).decode('utf-8')
    ext = path.split('.')[-1]
    return f"data:image/{ext};base64,{encoded}"

def convert_to_png(image_path):
    """
    Converts JPG/JPEG to PNG to avoid lossy compression issues.
    Returns new PNG path.
    """
    if image_path.lower().endswith(('.jpg', '.jpeg')):
        im = Image.open(image_path)
        png_path = os.path.splitext(image_path)[0] + ".png"
        im.save(png_path, format="PNG")
        return png_path
    return image_path

# ------------------------------
# Routes
# ------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/embed', methods=['POST'])
def embed():
    if 'cover' not in request.files or request.files['cover'].filename == '':
        flash("Please upload a valid image file.")
        return redirect(url_for('index'))

    cover_file = request.files['cover']
    message = request.form['message']
    output_format = request.form.get('output_format', 'PNG')  # from dropdown if added

    if not allowed_file(cover_file.filename):
        flash("Unsupported file format. Use PNG, BMP, JPG, or JPEG.")
        return redirect(url_for('index'))

    filename = secure_filename(cover_file.filename)
    uid = str(uuid.uuid4())[:8]
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{uid}_{filename}")
    cover_file.save(input_path)

    # Convert JPEGs internally to PNG
    input_path = convert_to_png(input_path)

    # Output file
    ext = output_format.lower()
    output_name = f"stego_{uid}.{ext}"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_name)

    success = hide_data(input_path, output_path, message, output_format)

    if not success:
        flash("Message too large for selected image. Try a larger one.")
        return redirect(url_for('index'))

    datauri = file_to_datauri(output_path)
    download_url = url_for('download_file', filename=output_name)
    return render_template('result.html',
                       stego_datauri=datauri,
                       stego_filename=output_name,
                       download_url=download_url)

@app.route('/extract', methods=['POST'])
def extract():
    if 'stego' not in request.files or request.files['stego'].filename == '':
        flash("Please upload a stego image.")
        return redirect(url_for('index'))

    stego_file = request.files['stego']
    if not allowed_file(stego_file.filename):
        flash("Unsupported file format.")
        return redirect(url_for('index'))

    filename = secure_filename(stego_file.filename)
    uid = str(uuid.uuid4())[:8]
    path = os.path.join(app.config['UPLOAD_FOLDER'], f"{uid}_{filename}")
    stego_file.save(path)

    message = extract_data(path)
    return render_template('extracted.html', message=message)

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'cover' not in request.files or 'stego' not in request.files:
        flash("Please upload both cover and stego images.")
        return redirect(url_for('index'))

    cover_file = request.files['cover']
    stego_file = request.files['stego']

    uid = str(uuid.uuid4())[:8]
    cover_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{uid}_cover.png")
    stego_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{uid}_stego.png")
    cover_file.save(cover_path)
    stego_file.save(stego_path)

    mse, psnr, hist_datauri = compare_images(cover_path, stego_path)
    return render_template('analysis.html', mse=mse, psnr=psnr, hist_datauri=hist_datauri)

from flask import send_from_directory
@app.route('/download/<filename>')
def download_file(filename):
    """Serve the stego image for download."""
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    app.run(debug=True)
