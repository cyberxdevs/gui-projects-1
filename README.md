# Aplikasi GUI Analisis Postur - Python YOLO

Aplikasi desktop berbasis Python untuk analisis postur tubuh menggunakan model YOLO dengan antarmuka GUI yang user-friendly.

## 📋 Deskripsi

Aplikasi ini dirancang untuk melakukan analisis postur tubuh secara otomatis menggunakan model YOLO (You Only Look Once). Aplikasi memiliki 4 dashboard utama yang memandu pengguna dari input data hingga hasil analisis lengkap dengan visualisasi dan export data.

## ✨ Fitur Utama

### Dashboard 1: Input Data
- Input nama lengkap pengguna
- Input tinggi badan (dalam mm)
- Logo dan tampilan profesional

### Dashboard 2: Upload & Konfigurasi
- Upload model YOLO (format .pt)
- Upload gambar (single atau batch)
- Menu analisis:
  - Analisis Single Image
  - Analisis Batch Image
- System Info
- Pengaturan confidence threshold dengan scrollbar
- Menu keluar

### Dashboard 3: Visualisasi Before/After
- Visualisasi gambar sebelum dan sesudah analisis
- Deteksi postur dengan bounding box
- Analisis keypoint detection
- Perhitungan imbalance postur:
  - Shoulder imbalance
  - Hip imbalance
  - Spine deviation
  - Head shift (untuk side view)
  - Head tilt (untuk side view)
- Output nilai imbalance dengan automation debug

### Dashboard 4: Hasil & Export
- Visualisasi gambar dengan anotasi lengkap
- Tabel hasil analisis imbalance postural:
  - Kolom: Komponen, Parameter, Nilai, Satuan, Status, Score
- Ringkasan hasil analisis:
  - Klasifikasi postural (Normal, Kyphosis, Lordosis, Swayback)
  - Rekomendasi berdasarkan analisis
- Export hasil ke CSV
- Navigasi untuk analisis baru

## 🏗️ Struktur Proyek

```
project/
├── main.py                      # Entry point aplikasi
├── requirements.txt             # Dependencies
├── README.md                    # Dokumentasi
├── INSTALLATION.md              # Panduan instalasi detail
├── CONTRIBUTING.md              # Panduan kontribusi
├── config/
│   └── config.py               # Konfigurasi aplikasi
├── assets/
│   └── logo.png                # Logo aplikasi
├── src/
│   ├── gui/
│   │   ├── dashboard_1.py      # Dashboard input nama & tinggi
│   │   ├── dashboard_2.py      # Dashboard upload & menu
│   │   ├── dashboard_3.py      # Dashboard visualisasi
│   │   └── dashboard_4.py      # Dashboard hasil & export
│   ├── analysis/
│   │   ├── yolo_analyzer.py    # YOLO inference wrapper
│   │   └── posture_analyzer.py # Analisis postur & keypoint
│   └── utils/
│       ├── image_utils.py      # Image processing utilities
│       └── export_utils.py     # Export ke CSV
├── models/                      # Folder untuk model YOLO .pt
└── exports/                     # Folder untuk hasil export CSV
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Jalankan Aplikasi

```bash
python main.py
```

Untuk panduan instalasi lengkap, lihat [INSTALLATION.md](INSTALLATION.md)

## 💻 Cara Menggunakan

### Workflow Penggunaan

1. **Dashboard 1 - Input Data**
   - Masukkan nama lengkap Anda
   - Masukkan tinggi badan dalam mm (contoh: 1700 untuk 170 cm)
   - Klik "MULAI ANALISIS"

2. **Dashboard 2 - Upload & Konfigurasi**
   - Klik "📂 Pilih Model YOLO" untuk upload model .pt
   - Pilih mode analisis (Single atau Batch)
   - Klik "📷 Pilih Gambar" untuk upload gambar
   - Atur confidence threshold menggunakan scrollbar (default: 0.25)
   - Klik "🔍 ANALYZE IMAGES" untuk memulai analisis

3. **Dashboard 3 - Visualisasi**
   - Tunggu proses analisis selesai
   - Lihat visualisasi Before/After
   - Baca informasi deteksi dan keypoint
   - Klik "📊 VIEW RESULTS" untuk melihat hasil lengkap

4. **Dashboard 4 - Hasil & Export**
   - Tab "Visualization": Lihat gambar hasil analisis
   - Tab "Analysis Table": Lihat tabel imbalance postural
   - Tab "Summary": Baca ringkasan dan rekomendasi
   - Klik "💾 Export to CSV" untuk export hasil
   - Klik "🔄 New Analysis" untuk analisis baru

## 📊 Mapping Klasifikasi Postural

Aplikasi melakukan mapping otomatis dari sub-kategori ke kategori utama:

| Sub-kategori | Kategori Utama |
|--------------|----------------|
| Normal-Kanan, Normal-Kiri, Normal-Belakang, Normal-Depan | **Normal** |
| Kyphosis-Kanan, Kyphosis-Kiri, Kyphosis-Belakang, Kyphosis-Depan | **Kyphosis** |
| Lordosis-Kanan, Lordosis-Kiri, Lordosis-Belakang, Lordosis-Depan | **Lordosis** |
| Swayback-Kanan, Swayback-Kiri, Swayback-Belakang, Swayback-Depan | **Swayback** |

## 🔍 Jenis Analisis

### Back/Front Analysis
Untuk postur tampak belakang atau depan:
- **Shoulder Imbalance**: Perbedaan tinggi bahu kiri dan kanan (mm)
- **Hip Imbalance**: Perbedaan tinggi pinggul kiri dan kanan (mm)
- **Spine Deviation**: Deviasi tulang belakang dari garis tengah (mm)

### Side Analysis
Untuk postur tampak samping:
- **Head Shift**: Pergeseran kepala ke depan/belakang (mm)
- **Head Tilt**: Kemiringan kepala (derajat)

## 🎯 Scoring System

Aplikasi memberikan score 0-100 untuk setiap komponen:

| Nilai Imbalance | Status | Score |
|----------------|--------|-------|
| < 10 mm / 5° | Normal | 100 |
| 10-20 mm / 5-10° | Ringan | 75 |
| 20-30 mm / 10-15° | Sedang | 50 |
| > 30 mm / 15° | Berat | 25 |

**Overall Score**: Rata-rata dari semua komponen

## 🛡️ Automation Debug

Aplikasi dilengkapi dengan automation debug untuk head alignment yang memastikan:
- Nilai imbalance tetap realistis
- Outlier data dikoreksi otomatis
- Hasil analisis konsisten dan akurat

## 📁 Export Format

File CSV yang diexport memiliki struktur:

| Komponen | Parameter | Nilai | Satuan | Status | Score |
|----------|-----------|-------|--------|--------|-------|
| Shoulder Imbalance | Perbedaan Tinggi Bahu | 2.5 | mm | Normal | 100/100 |

Nama file: `{nama_user}_{timestamp}_analisis_postur.csv`

## 🌐 Integrasi Web

Aplikasi ini dapat diintegrasikan ke website dengan beberapa cara:

### 1. Flask/Django Backend
Convert logic analysis ke REST API

### 2. Streamlit Web App
Convert GUI ke Streamlit untuk web deployment

### 3. FastAPI + React
Backend FastAPI + Frontend React untuk deployment cloud

Lihat dokumentasi lengkap untuk detail integrasi web.

## 📝 Dependencies

- opencv-python >= 4.8.0
- ultralytics >= 8.0.0
- pillow >= 10.0.0
- pandas >= 2.0.0
- numpy >= 1.24.0
- matplotlib >= 3.7.0

## 🔧 Troubleshooting

Lihat [INSTALLATION.md](INSTALLATION.md) untuk troubleshooting lengkap.

## 👥 Kontribusi

Kami menerima kontribusi! Lihat [CONTRIBUTING.md](CONTRIBUTING.md) untuk guidelines.

## 📝 Lisensi

© 2024 Aplikasi Analisis Postur - Powered by YOLO

## 📧 Kontak & Support

Untuk pertanyaan atau dukungan, silakan buat issue di repository ini.

---

**Made with ❤️ using Python & YOLO**