# 🕵️‍♂️ Secure LSB Steganography Project

A **Python + Flask** web application for **Steganography Embedding and Detection** using the **Least Significant Bit (LSB)** technique — now enhanced with **AES-GCM encryption**, **RSA public-key wrapping**, and **random pixel selection** for improved security and confidentiality.

Developed for the *Multimedia Forensics Lab Final Evaluation*, this project demonstrates how sensitive data can be hidden securely within digital images while maintaining high visual fidelity.

---

## ✨ Features

* 🧩 **Secure Embedding with AES-GCM:**  
  Secret messages are encrypted using AES before embedding to ensure confidentiality.

* 🔐 **RSA Key Wrapping:**  
  AES + randomization keys are encrypted using the receiver’s RSA public key, so only the receiver’s private key can decrypt them.

* 🎲 **Random Pixel Selection:**  
  Pixel embedding positions are randomized using a secret key shared only between sender and receiver.

* 🖼️ **Automatic JPEG-to-PNG Conversion:**  
  JPEG/JPG images are automatically converted to PNG to prevent data loss due to compression.

* 📊 **Steganalysis Dashboard:**  
  Compare cover and stego images using **Histogram**, **MSE**, and **PSNR** metrics.

* 🧮 **Dynamic Capacity Display:**  
  Shows how many characters can safely be hidden in the selected image before embedding.

* 🌐 **Modern Web Frontend:**  
  Built with Flask + HTML/CSS for simplicity, clarity, and accessibility.

---

## 🛠️ Tech Stack

| Component | Technology |
| ---------- | ----------- |
| **Language** | Python 3.10+ |
| **Framework** | Flask |
| **Libraries** | OpenCV, NumPy, Pillow, Matplotlib, PyCryptodome |
| **Frontend** | HTML, CSS (custom minimalist UI) |
| **Platform** | Localhost (can deploy to Render / PythonAnywhere) |

---

## 📂 Folder Structure

```
LSB_Steganography_Project/
│
├── backend/
│ ├── encode.py # LSB embedding logic (supports random pixel selection)
│ ├── decode.py # LSB extraction logic
│ ├── crypto_utils.py # AES-GCM + RSA key wrapping/unwrapping
│ ├── analysis.py # Histogram, PSNR, MSE
│ └── utils.py # Common helper functions
│
├── webapp/
│ ├── app.py # Flask server & routes
│ ├── templates/ # HTML pages (index, result, extract, analysis)
│ └── static/ # CSS & assets
│
├── input/ # Uploaded cover images
├── output/ # Generated stego images
├── key_generation.py # code for generating keys
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Run Locally

### 🧱 1. Clone Repository

```bash
git clone https://github.com/<your-username>/LSB_Steganography_Project.git
cd LSB_Steganography_Project
```

### 💻 2. Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate    # (Windows)
source .venv/bin/activate # (Linux/Mac)
```

### ⚙️ 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 🌐 4. Run Flask App

```bash
cd webapp
python app.py
```

Then open your browser → `http://127.0.0.1:5000`

---

## 🧠 How It Works

| Stage                    | Description                                                                                                                             |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| **1️⃣ Embedding**        | Converts the secret message to binary, encrypts it using AES-GCM, and embeds it in the least significant bits of random pixel channels. |
| **2️⃣ RSA Key Wrapping** | The AES and randomization keys are wrapped (encrypted) using the receiver’s RSA public key and shared as a base64 “wrapped blob.”       |
| **3️⃣ Extraction**       | The receiver uploads the stego image, private key, and wrapped blob. The system unwraps and decrypts the hidden message.                |
| **4️⃣ Steganalysis**     | Computes MSE, PSNR, and histogram similarity to evaluate imperceptibility.                                                              |

## 🔑 Secure Workflow
---

### 🧾 **Receiver (Generate RSA Keys)**

```python
from Crypto.PublicKey import RSA

# Generate RSA key pair
key = RSA.generate(2048)

# Save private and public keys
open("receiver_private.pem", "wb").write(key.export_key())
open("receiver_public.pem", "wb").write(key.publickey().export_key())
```
same code is in key_generation.py, run it to get the files
* Share `receiver_public.pem` with the sender.
* Keep `receiver_private.pem` safe and private.

**💻 Sender (Embed Securely)**

* Upload a cover image (`.png`, `.jpg`, `.jpeg`, `.bmp`)
* Enter the secret message
* Upload the receiver’s public key file (receiver_public.pem)
* Click Embed Securely
* Download the stego image and copy the wrapped key blob

**🕵️‍♂️ Receiver (Extract Message)**

* Upload the stego image
* Upload your private key (.pem)
* Paste the wrapped key blob
* Click Extract & Decrypt

---

## 👥 Team Members

* **Maithil Mishra** 
* **[Piyush Deshpande](https://github.com/Piyush3012)**
* **[Shresth Raj](https://github.com/KrShresth)**

---

## 💬 Acknowledgements

This project was developed as part of the **Multimedia Forensics** coursework under guidance from the faculty at *IIIT Kottayam*.

---

## 🧩 Future Enhancements

* 🧠 Password-based AES key generation (PBKDF2)
* 📈 PDF report generation for steganalysis results
* 🧮 Advanced methods – DCT/DWT-based embedding
* 🎨 Enhanced UI with progress bar and visual comparison slider
* ☁️ Online sharing with receiver key auto-transfer

---

## 📜 License

This project is released under the **MIT License** – free to use, modify, and share for academic purposes.

---

