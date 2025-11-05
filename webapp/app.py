# webapp/app.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.analysis import compare_images
import uuid
import base64
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash
from werkzeug.utils import secure_filename
from backend.encode import hide_data
from backend.decode import extract_data

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'input')
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'output')
ALLOWED_EXT = {'png', 'bmp'}  # lossless

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = 'dev-secret-key'  # change for production
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


def file_to_datauri(path):
    with open(path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode('utf-8')
    ext = path.rsplit('.', 1)[1].lower()
    return f"data:image/{ext};base64,{b64}"


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/embed', methods=['POST'])
def embed():
    if 'cover_image' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    file = request.files['cover_image']
    message = request.form.get('message', '')
    if file.filename == '' or message.strip() == '':
        flash('Please provide both an image and a message.')
        return redirect(url_for('index'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # make name unique
        uid = uuid.uuid4().hex[:8]
        cover_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{uid}_{filename}")
        file.save(cover_path)
        outname = f"stego_{uid}_{filename}"
        outpath = os.path.join(app.config['OUTPUT_FOLDER'], outname)

        success = hide_data(cover_path, outpath, message)
        if not success:
            flash('Message too large to embed in selected image. Choose larger image or shorter message.')
            return redirect(url_for('index'))

        datauri = file_to_datauri(outpath)
        return render_template('result.html', stego_datauri=datauri, stego_filename=outname)
    else:
        flash('Invalid file type. Upload PNG or BMP (lossless).')
        return redirect(url_for('index'))


@app.route('/extract', methods=['POST'])
def extract():
    if 'stego_image' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    file = request.files['stego_image']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        uid = uuid.uuid4().hex[:8]
        stego_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{uid}_{filename}")
        file.save(stego_path)
        try:
            message = extract_data(stego_path)
        except Exception as e:
            flash(f'Error extracting message: {e}')
            return redirect(url_for('index'))
        return render_template('result.html', extracted_message=message)
    else:
        flash('Invalid file type. Upload PNG or BMP (lossless).')
        return redirect(url_for('index'))
    
@app.route('/analyze', methods=['POST'])
def analyze():
    cover_file = request.files.get('cover_image')
    stego_file = request.files.get('stego_image')
    if not cover_file or not stego_file:
        flash('Please upload both cover and stego images.')
        return redirect(url_for('index'))

    if not (allowed_file(cover_file.filename) and allowed_file(stego_file.filename)):
        flash('Only PNG or BMP images allowed.')
        return redirect(url_for('index'))

    uid = uuid.uuid4().hex[:8]
    cover_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{uid}_cover_{secure_filename(cover_file.filename)}")
    stego_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{uid}_stego_{secure_filename(stego_file.filename)}")
    cover_file.save(cover_path)
    stego_file.save(stego_path)

    try:
        mse_val, psnr_val, hist_img = compare_images(cover_path, stego_path)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))

    return render_template(
        'result.html',
        analysis_mode=True,
        mse=round(mse_val, 2),
        psnr=round(psnr_val, 2),
        hist_image=hist_img
    )


@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
