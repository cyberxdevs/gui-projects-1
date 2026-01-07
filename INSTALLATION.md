# Panduan Instalasi Detail

Dokumen ini memberikan panduan lengkap untuk instalasi dan menjalankan aplikasi GUI Analisis Postur di VSCode.

## 📋 Prerequisites

Sebelum memulai, pastikan sistem Anda memiliki:

1. **Python 3.8 atau lebih tinggi**
   - Download dari: https://www.python.org/downloads/
   - Saat instalasi, centang "Add Python to PATH"

2. **pip (Python Package Manager)**
   - Biasanya sudah terinstall dengan Python
   - Cek dengan: `pip --version`

3. **Visual Studio Code**
   - Download dari: https://code.visualstudio.com/

4. **Git** (optional, untuk clone repository)
   - Download dari: https://git-scm.com/

## 🔧 Langkah Instalasi

### 1. Setup Project

#### Opsi A: Clone dari Repository
```bash
git clone <repository-url>
cd gui-projects-1
```

#### Opsi B: Download ZIP
1. Download ZIP dari repository
2. Extract ke folder pilihan Anda
3. Buka terminal/command prompt di folder tersebut

### 2. Buka di VSCode

```bash
code .
```

Atau buka VSCode dan pilih File > Open Folder, lalu pilih folder project.

### 3. Setup Virtual Environment (Recommended)

Virtual environment membantu mengisolasi dependencies project.

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

Anda akan melihat `(venv)` di awal command prompt, menandakan virtual environment aktif.

### 4. Install Dependencies

Dengan virtual environment aktif, install semua dependencies:

```bash
pip install -r requirements.txt
```

Ini akan menginstall:
- opencv-python (untuk image processing)
- ultralytics (untuk YOLO)
- pillow (untuk GUI image handling)
- pandas (untuk export CSV)
- numpy (untuk numerical operations)
- matplotlib (untuk plotting)

**Catatan**: Proses ini mungkin memakan waktu beberapa menit tergantung koneksi internet.

### 5. Verifikasi Instalasi

Cek apakah semua package terinstall dengan benar:

```bash
pip list
```

Atau test import:

```bash
python -c "import cv2, ultralytics, PIL, pandas, numpy; print('All packages imported successfully!')"
```

### 6. Setup Model YOLO

1. Siapkan model YOLO Anda (format .pt)
2. Letakkan di folder `models/` (atau siapkan untuk diupload via aplikasi)

Struktur folder:
```
gui-projects-1/
├── models/
│   └── your_model.pt    # Letakkan model di sini
```

## 🚀 Menjalankan Aplikasi

### Di Terminal/Command Prompt

```bash
python main.py
```

Atau:

```bash
python3 main.py
```

### Di VSCode

#### Cara 1: Menggunakan Play Button
1. Buka file `main.py`
2. Klik tombol ▶️ (Run Python File) di pojok kanan atas
3. Atau tekan `Ctrl+F5` (Windows/Linux) atau `Cmd+F5` (macOS)

#### Cara 2: Menggunakan Terminal Integrated
1. Buka terminal di VSCode (Terminal > New Terminal)
2. Pastikan virtual environment aktif
3. Jalankan: `python main.py`

## 🐛 Troubleshooting

### Error: "python" tidak dikenali

**Solusi:**
- Windows: Install Python dan centang "Add to PATH" saat instalasi
- Atau gunakan: `py main.py`
- macOS/Linux: Gunakan `python3` instead of `python`

### Error: "No module named 'cv2'"

**Solusi:**
```bash
pip install opencv-python
```

### Error: "No module named 'ultralytics'"

**Solusi:**
```bash
pip install ultralytics
```

### Error: "Tkinter not found"

**Solusi:**

**Windows**: Tkinter biasanya sudah include dengan Python

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**macOS:**
```bash
brew install python-tk
```

### Error: "ImportError: DLL load failed"

**Solusi (Windows):**
1. Install Visual C++ Redistributable:
   - https://aka.ms/vs/17/release/vc_redist.x64.exe
2. Restart komputer

### Aplikasi tidak muncul / crash saat startup

**Solusi:**
1. Pastikan semua dependencies terinstall
2. Cek error message di terminal
3. Coba hapus folder `__pycache__` dan jalankan ulang
4. Pastikan tidak ada conflict dengan Python lain

### Permission denied saat membuat folder

**Solusi:**
- Windows: Jalankan CMD/PowerShell sebagai Administrator
- macOS/Linux: Gunakan `sudo` atau ubah permission folder

## 📦 Instalasi untuk Development

Jika Anda ingin develop aplikasi:

### 1. Install Development Tools

```bash
pip install pylint black autopep8
```

### 2. Setup VSCode Extensions

Install extension berikut di VSCode:
- Python (Microsoft)
- Pylance
- Python Indent
- GitLens (optional)

### 3. Configure VSCode Settings

Buat file `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true
}
```

## 🔄 Update Dependencies

Untuk update dependencies ke versi terbaru:

```bash
pip install --upgrade -r requirements.txt
```

## 🗑️ Uninstall

Untuk menghapus virtual environment dan dependencies:

### Windows:
```bash
deactivate
rmdir /s venv
```

### macOS/Linux:
```bash
deactivate
rm -rf venv
```

## 📊 System Requirements

### Minimum:
- OS: Windows 7+, macOS 10.12+, Ubuntu 16.04+
- RAM: 4 GB
- Storage: 2 GB free space
- Python: 3.8+

### Recommended:
- OS: Windows 10+, macOS 11+, Ubuntu 20.04+
- RAM: 8 GB
- Storage: 5 GB free space
- Python: 3.9+
- GPU: NVIDIA GPU dengan CUDA support (optional, untuk inference lebih cepat)

## 🎓 Catatan Penting

1. **Virtual Environment**: Selalu gunakan virtual environment untuk menghindari conflict dependencies
2. **Python Version**: Pastikan menggunakan Python 3.8 atau lebih tinggi
3. **Model YOLO**: Model harus sudah dilatih dan dalam format .pt
4. **Image Format**: Gunakan format JPG, PNG, atau BMP untuk gambar input
5. **File Permission**: Pastikan aplikasi memiliki permission untuk read/write file

## 📞 Bantuan Lebih Lanjut

Jika masih mengalami masalah:
1. Cek error message lengkap di terminal
2. Baca documentation dependencies (OpenCV, Ultralytics)
3. Buat issue di repository dengan detail error

---

**Selamat menggunakan Aplikasi Analisis Postur!** 🎉
