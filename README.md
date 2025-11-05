# 🕵️‍♂️ LSB Steganography Project

A **Python + Flask** based web application for **Steganography Embedding and Detection** using the **Least Significant Bit (LSB)** technique.
This project was developed for the *Multimedia Forensics Lab Final Evaluation* and demonstrates secure data hiding within digital images while maintaining high visual fidelity.

---

## ✨ Features

* 🧩 **Embed Secret Messages** into PNG/BMP images using LSB substitution
* 🔍 **Extract Hidden Data** from stego images accurately
* 📊 **Steganalysis Module** – compare cover and stego images (Histogram, MSE, PSNR)
* 🌐 **Web Frontend** built with Flask + HTML/CSS
* ⚡ **Optional Desktop GUI** (Tkinter) for offline use

---

## 🛠️ Tech Stack

| Component | Technology                                        |
| --------- | ------------------------------------------------- |
| Language  | Python 3.10+                                      |
| Libraries | Flask, OpenCV, NumPy, Matplotlib, Pillow          |
| Frontend  | HTML, CSS (custom minimalist UI)                  |
| Platform  | Localhost (can deploy to Render / PythonAnywhere) |

---

## 📂 Folder Structure

```
LSB_Steganography_Project/
│
├── backend/
│   ├── encode.py          # Embed logic
│   ├── decode.py          # Extract logic
│   ├── analysis.py        # Histogram, PSNR, MSE
│   └── utils.py           # Shared helpers
│
├── webapp/
│   ├── app.py             # Flask server
│   ├── templates/         # HTML files
│   └── static/            # CSS & assets
│
├── input/                 # User-uploaded cover images
├── output/                # Generated stego images
└── README.md
```

---

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

| Stage            | Description                                                                                |
| ---------------- | ------------------------------------------------------------------------------------------ |
| **Embedding**    | Converts text message into binary and replaces the least significant bits of pixel values. |
| **Detection**    | Reads LSBs of image pixels and reconstructs the hidden binary message.                     |
| **Steganalysis** | Calculates MSE/PSNR and shows histogram similarity between cover and stego images.         |


## 👥 Team Members

* **Maithil Mishra** 
* **[Piyush Deshpande](https://github.com/Piyush3012)**

---

## 💬 Acknowledgements

This project was developed as part of the **Multimedia Forensics** coursework under guidance from the faculty at *IIIT Kottayam*.

---

## 🧩 Future Enhancements

* 🔐 Add AES encryption for messages before embedding
* 🖼️ Support for video-based steganography
* 📈 Enhanced statistical steganalysis (Chi-square, RS analysis)

---

## 📜 License

This project is released under the **MIT License** – free to use, modify, and share for academic purposes.

---

```
