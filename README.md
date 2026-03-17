# 📸 Photo Contact Sheet Generator

Generate printable A4 photo sheets directly from Google Drive using Google Colab.

---

## 🚀 Run in Google Colab

Click below to launch the notebook instantly:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shovon05/photo-contact-sheet/blob/main/colab_runner.ipynb)

---

## ✨ Features

- 📷 Supports JPG, JPEG, PNG, HEIC
- 📄 Generates printable A4 PDF sheets
- 📏 Adjustable photo size (1–4 inches)
- 📐 Optional margins
- ⚡ Handles 1000+ images efficiently
- ☁️ Direct Google Drive integration
- 🧠 Auto-rotation for better fit

---

## 📂 Required Folder Structure (Google Drive)

Your photos must be placed in the following structure:
MyDrive/
└── photos/
├── image1.jpg
├── image2.png
├── image3.heic
└── ...


### ⚠️ Important Notes

- Folder name must be exactly: `photos`
- Path used in the notebook: /content/drive/MyDrive/photos

- Do NOT create subfolders inside `photos`
- Supported formats:
- JPG / JPEG
- PNG
- HEIC

---

## 📄 Output

The generated PDF will be saved to: MyDrive/photo_sheets.pdf




---

## 🛠️ How It Works

1. Open the notebook in Google Colab
2. Mount your Google Drive
3. Enter:
   - photo size (in inches)
   - margin preference
4. Run the script
5. Download or print your PDF

---

## 🖨️ Printing Instructions

For correct dimensions:

- Paper size: **A4**
- Scale: **100% / Actual size**
- Disable: **Fit to page**

---

## 📦 Tech Stack

- Python
- Pillow (PIL)
- pillow-heif (HEIC support)
- Google Colab
- Google Drive

---

## 🚧 Future Improvements

- 🎛️ Interactive UI (dropdowns, buttons)
- 🧩 Smart packing (masonry layout)
- ⚡ Faster batch processing
- 📊 Preview before export

---

## 👨‍💻 Author

**Shovon**

---

## ⭐ If you find this useful

Give it a star ⭐ on GitHub — it helps a lot!
