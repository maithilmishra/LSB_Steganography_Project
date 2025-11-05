# backend/analysis.py
import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

def mse(imageA, imageB):
    """Mean Squared Error between two images."""
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

def psnr(imageA, imageB):
    """Peak Signal-to-Noise Ratio."""
    m = mse(imageA, imageB)
    if m == 0:
        return float("inf")
    max_pixel = 255.0
    return 20 * np.log10(max_pixel / np.sqrt(m))

def compare_images(cover_path: str, stego_path: str):
    """
    Compare cover and stego images visually and numerically.
    Returns (MSE, PSNR, histogram_base64)
    """
    cover = cv2.imread(cover_path)
    stego = cv2.imread(stego_path)
    if cover is None or stego is None:
        raise FileNotFoundError("Could not read one of the images for comparison.")

    # Resize to same shape if needed
    if cover.shape != stego.shape:
        stego = cv2.resize(stego, (cover.shape[1], cover.shape[0]))

    m = mse(cover, stego)
    p = psnr(cover, stego)

    # Plot histogram comparison
    plt.figure(figsize=(6, 4))
    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        hist_cover = cv2.calcHist([cover], [i], None, [256], [0, 256])
        hist_stego = cv2.calcHist([stego], [i], None, [256], [0, 256])
        plt.plot(hist_cover, color=col, linestyle='--', label=f'{col.upper()} Cover')
        plt.plot(hist_stego, color=col, label=f'{col.upper()} Stego')
    plt.legend()
    plt.title("Histogram Comparison")
    plt.xlabel("Pixel Intensity")
    plt.ylabel("Frequency")

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    hist_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    hist_datauri = f"data:image/png;base64,{hist_base64}"

    return round(m, 4), round(p, 2), hist_datauri
