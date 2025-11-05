# backend/analysis.py
import cv2
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

def psnr(imageA, imageB):
    mse_val = mse(imageA, imageB)
    if mse_val == 0:
        return float('inf')
    max_pixel = 255.0
    return 20 * np.log10(max_pixel / np.sqrt(mse_val))

def compare_images(cover_path, stego_path):
    """Compute PSNR, MSE and generate histogram comparison plot as base64."""
    cover = cv2.imread(cover_path)
    stego = cv2.imread(stego_path)

    if cover is None or stego is None:
        raise ValueError("Error: One or both images not found or invalid.")

    cover = cv2.resize(cover, (stego.shape[1], stego.shape[0]))  # ensure same size

    mse_val = mse(cover, stego)
    psnr_val = psnr(cover, stego)

    # Plot histograms
    plt.figure(figsize=(8, 4))
    plt.hist(cover.ravel(), bins=256, color='blue', alpha=0.5, label='Cover')
    plt.hist(stego.ravel(), bins=256, color='red', alpha=0.5, label='Stego')
    plt.title("Histogram Comparison")
    plt.xlabel("Pixel Intensity")
    plt.ylabel("Frequency")
    plt.legend()

    # Convert plot to base64 string for HTML embedding
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')

    return mse_val, psnr_val, img_base64
