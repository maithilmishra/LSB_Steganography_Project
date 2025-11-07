import cv2
import numpy as np
import io, base64
import matplotlib.pyplot as plt

def analyze_images(cover_path, stego_path):
    img1 = cv2.imread(cover_path)
    img2 = cv2.imread(stego_path)
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        psnr = 100
    else:
        psnr = 20 * np.log10(255.0 / np.sqrt(mse))

    plt.figure(figsize=(6, 3))
    plt.hist(img1.ravel(), 256, [0, 256], alpha=0.5, label='Cover')
    plt.hist(img2.ravel(), 256, [0, 256], alpha=0.5, label='Stego')
    plt.legend()
    plt.title('Pixel Intensity Histogram')
    plt.xlabel('Intensity Value')
    plt.ylabel('Frequency')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    hist_datauri = 'data:image/png;base64,' + base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    return round(mse, 4), round(psnr, 4), hist_datauri
