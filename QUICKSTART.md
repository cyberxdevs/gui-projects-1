# Quick Start Guide

Panduan cepat untuk memulai aplikasi GUI Analisis Postur.

## 🚀 Setup Cepat (5 Menit)

### 1. Install Python

Pastikan Python 3.8+ terinstall:

```bash
python --version
# atau
python3 --version
```

Jika belum, download dari: https://www.python.org/downloads/

### 2. Install Dependencies

```bash
# Buat virtual environment (recommended)
python -m venv venv

# Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Siapkan Model YOLO

Letakkan model YOLO Anda (file `.pt`) di folder `models/` atau siapkan untuk upload via aplikasi.

### 4. Jalankan Aplikasi

```bash
python main.py
```

## 📝 Penggunaan Cepat

### Step 1: Input Data
1. Masukkan nama lengkap
2. Masukkan tinggi badan dalam mm (contoh: `1700` untuk 170 cm)
3. Klik **MULAI ANALISIS**

### Step 2: Upload & Analisis
1. Klik **📂 Pilih Model YOLO** → Pilih file `.pt`
2. Pilih mode: Single atau Batch
3. Klik **📷 Pilih Gambar** → Pilih gambar postur
4. (Optional) Atur confidence threshold
5. Klik **🔍 ANALYZE IMAGES**

### Step 3: Lihat Hasil
1. Tunggu analisis selesai
2. Lihat visualisasi Before/After
3. Klik **📊 VIEW RESULTS**

### Step 4: Export
1. Lihat tabel hasil analisis
2. Baca ringkasan dan rekomendasi
3. Klik **💾 Export to CSV** untuk export hasil

## 💡 Tips

- Gunakan gambar dengan resolusi tinggi untuk hasil terbaik
- Model YOLO harus mendukung keypoint detection (17 points)
- File gambar yang didukung: JPG, PNG, BMP
- Hasil CSV disimpan di folder `exports/`

## ❓ Troubleshooting Cepat

**Error: Module not found**
```bash
pip install -r requirements.txt
```

**Error: tkinter not found (Linux)**
```bash
sudo apt-get install python3-tk
```

**Aplikasi tidak muncul**
- Pastikan virtual environment aktif
- Check error di terminal
- Pastikan Python 3.8+

## 📚 Dokumentasi Lengkap

- [README.md](README.md) - Dokumentasi lengkap
- [INSTALLATION.md](INSTALLATION.md) - Panduan instalasi detail
- [ARCHITECTURE.md](ARCHITECTURE.md) - Dokumentasi arsitektur
- [PROJECT_STRUCTURE.txt](PROJECT_STRUCTURE.txt) - Struktur project

## 🎯 Format Output

### CSV Export
File CSV berisi tabel dengan kolom:
- Komponen (Shoulder, Hip, Spine, Head)
- Parameter (deskripsi)
- Nilai (angka)
- Satuan (mm atau derajat)
- Status (Normal/Ringan/Sedang/Berat)
- Score (0-100)

### Klasifikasi Postur
- **Normal**: Postur baik
- **Kyphosis**: Bungkuk (rounded shoulders)
- **Lordosis**: Lordosis (swayback)
- **Swayback**: Swayback posture

## 🔄 Mulai Analisis Baru

Dari Dashboard 4:
1. Klik **🔄 New Analysis** untuk kembali ke Dashboard 1
2. Atau klik **🔙 Back to Upload** untuk Dashboard 2

## 💻 VSCode Integration

### Run di VSCode
1. Buka folder project di VSCode
2. Buka `main.py`
3. Klik ▶️ (Run) atau tekan `F5`

### Setup VSCode
1. Install extension: "Python" (Microsoft)
2. Select Python interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter"
3. Pilih interpreter dari virtual environment

## 🌐 Integrasi Web (Advanced)

### Option 1: Flask
```python
from flask import Flask, request, jsonify
from src.analysis.yolo_analyzer import YOLOAnalyzer
from src.analysis.posture_analyzer import PostureAnalyzer

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    # Implementation
    pass
```

### Option 2: Streamlit
```python
import streamlit as st
from src.analysis.yolo_analyzer import YOLOAnalyzer

st.title("Analisis Postur")
uploaded_file = st.file_uploader("Upload Image")
# Implementation
```

## 📞 Need Help?

1. Check [INSTALLATION.md](INSTALLATION.md) untuk troubleshooting
2. Baca [README.md](README.md) untuk dokumentasi lengkap
3. Create issue di GitHub repository
4. Check error messages di terminal

---

**Selamat menganalisis! 🎉**
