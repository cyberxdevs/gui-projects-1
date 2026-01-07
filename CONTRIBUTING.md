# Contributing Guidelines

Terima kasih atas minat Anda untuk berkontribusi pada Aplikasi GUI Analisis Postur!

## 🤝 Cara Berkontribusi

### 1. Fork Repository

1. Fork repository ini ke akun GitHub Anda
2. Clone fork Anda ke local machine:
```bash
git clone https://github.com/your-username/gui-projects-1.git
cd gui-projects-1
```

### 2. Setup Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install development tools
pip install pylint black autopep8
```

### 3. Create Feature Branch

```bash
git checkout -b feature/nama-fitur-anda
```

### 4. Make Changes

- Tulis code yang clean dan readable
- Follow Python PEP 8 style guide
- Tambahkan docstrings untuk functions dan classes
- Test code Anda sebelum commit

### 5. Commit Changes

```bash
git add .
git commit -m "feat: deskripsi singkat perubahan"
```

**Commit Message Format:**
- `feat:` untuk fitur baru
- `fix:` untuk bug fixes
- `docs:` untuk dokumentasi
- `style:` untuk formatting
- `refactor:` untuk refactoring code
- `test:` untuk menambah tests
- `chore:` untuk maintenance tasks

### 6. Push to GitHub

```bash
git push origin feature/nama-fitur-anda
```

### 7. Create Pull Request

1. Buka repository Anda di GitHub
2. Klik "New Pull Request"
3. Pilih base repository dan branch
4. Berikan deskripsi detail tentang perubahan Anda
5. Submit pull request

## 📝 Code Style Guidelines

### Python Style

```python
# Good
def analyze_posture(image_path, model_path, confidence=0.25):
    """
    Analyze posture from image using YOLO model.

    Args:
        image_path (str): Path to image file
        model_path (str): Path to YOLO model
        confidence (float): Confidence threshold

    Returns:
        dict: Analysis results
    """
    # Implementation
    pass

# Bad
def analyze(img, mdl, conf=0.25):
    # No docstring
    pass
```

### Naming Conventions

- **Classes**: PascalCase (`PostureAnalyzer`)
- **Functions**: snake_case (`analyze_posture`)
- **Constants**: UPPER_SNAKE_CASE (`DEFAULT_CONFIDENCE`)
- **Variables**: snake_case (`image_path`)

### File Organization

- Satu class per file untuk class besar
- Group related functions
- Import order: standard library, third-party, local

## 🧪 Testing

Sebelum submit PR, test aplikasi Anda:

1. **Manual Testing**
   - Test semua dashboard
   - Test dengan berbagai input
   - Test error handling

2. **Code Quality**
   ```bash
   # Check style
   pylint src/

   # Format code
   black src/
   ```

## 🐛 Reporting Bugs

Jika menemukan bug, buat issue dengan:

1. **Deskripsi jelas** tentang bug
2. **Steps to reproduce**
3. **Expected vs actual behavior**
4. **Screenshots** (jika applicable)
5. **Environment info** (OS, Python version, dll)

Template:
```markdown
**Bug Description:**
[Deskripsi singkat]

**Steps to Reproduce:**
1. Buka dashboard 2
2. Upload model
3. ...

**Expected Behavior:**
[Apa yang seharusnya terjadi]

**Actual Behavior:**
[Apa yang sebenarnya terjadi]

**Environment:**
- OS: Windows 10
- Python: 3.9.5
- Dependencies: [list versions]

**Screenshots:**
[Attach screenshots]
```

## 💡 Feature Requests

Untuk request fitur baru:

1. Cek apakah sudah ada issue serupa
2. Buat issue baru dengan label "enhancement"
3. Jelaskan use case dan benefit

## 📋 Checklist sebelum Submit PR

- [ ] Code follows style guidelines
- [ ] Docstrings added/updated
- [ ] Manual testing completed
- [ ] No console errors
- [ ] README updated (if needed)
- [ ] No breaking changes (or documented)

## 🔍 Code Review Process

1. Maintainer akan review PR Anda
2. Mungkin ada request untuk changes
3. Setelah approved, PR akan di-merge
4. Anda akan dikreditkan sebagai contributor!

## 📧 Questions?

Jika ada pertanyaan, feel free to:
- Open an issue
- Comment di PR Anda
- Contact maintainers

## 🙏 Terima Kasih!

Setiap kontribusi, sekecil apapun, sangat dihargai! Terima kasih telah membantu improve aplikasi ini.

---

**Happy Contributing!** 🎉
