"""
Dashboard 2 - Upload Images dan Menu Analisis
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from config.config import *


class Dashboard2(tk.Frame):
    """Dashboard kedua untuk upload images dan menu analisis"""

    def __init__(self, parent, app_controller):
        super().__init__(parent, bg=BG_COLOR)
        self.parent = parent
        self.app_controller = app_controller

        self.selected_images = []
        self.model_path = None
        self.confidence = tk.DoubleVar(value=DEFAULT_CONFIDENCE)
        self.analysis_mode = tk.StringVar(value="single")

        self.setup_ui()

    def setup_ui(self):
        """Setup UI components"""
        # Header
        header_frame = tk.Frame(self, bg=PRIMARY_COLOR)
        header_frame.pack(fill='x', pady=(0, 20))

        header_content = tk.Frame(header_frame, bg=PRIMARY_COLOR)
        header_content.pack(pady=20)

        title_label = tk.Label(
            header_content,
            text="DASHBOARD ANALISIS POSTUR",
            font=('Arial', 24, 'bold'),
            bg=PRIMARY_COLOR,
            fg='white'
        )
        title_label.pack()

        user_data = self.app_controller.get_user_data()
        if user_data:
            user_label = tk.Label(
                header_content,
                text=f"User: {user_data['name']} | Height: {user_data['height']} mm",
                font=('Arial', 12),
                bg=PRIMARY_COLOR,
                fg='white'
            )
            user_label.pack()

        # Main container
        main_container = tk.Frame(self, bg=BG_COLOR)
        main_container.pack(expand=True, fill='both', padx=30, pady=20)

        # Left panel - Menu
        left_panel = tk.Frame(main_container, bg='white', relief='raised', borderwidth=2)
        left_panel.pack(side='left', fill='y', padx=(0, 20), ipadx=20, ipady=20)

        self.create_menu(left_panel)

        # Right panel - Upload dan controls
        right_panel = tk.Frame(main_container, bg='white', relief='raised', borderwidth=2)
        right_panel.pack(side='right', expand=True, fill='both', padx=20, ipadx=20, ipady=20)

        self.create_upload_section(right_panel)

    def create_menu(self, parent):
        """Create menu panel"""
        menu_title = tk.Label(
            parent,
            text="MENU",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg=PRIMARY_COLOR
        )
        menu_title.pack(pady=(10, 20))

        # Analysis mode
        mode_label = tk.Label(
            parent,
            text="Mode Analisis:",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg=PRIMARY_COLOR
        )
        mode_label.pack(pady=(0, 10), anchor='w')

        single_radio = tk.Radiobutton(
            parent,
            text="📄 Single Image Analysis",
            variable=self.analysis_mode,
            value="single",
            font=('Arial', 11),
            bg='white',
            activebackground='white'
        )
        single_radio.pack(anchor='w', pady=5)

        batch_radio = tk.Radiobutton(
            parent,
            text="📁 Batch Image Analysis",
            variable=self.analysis_mode,
            value="batch",
            font=('Arial', 11),
            bg='white',
            activebackground='white'
        )
        batch_radio.pack(anchor='w', pady=5)

        # Separator
        ttk.Separator(parent, orient='horizontal').pack(fill='x', pady=20)

        # System info button
        sysinfo_btn = tk.Button(
            parent,
            text="ℹ️  System Info",
            font=('Arial', 11),
            bg=SECONDARY_COLOR,
            fg='white',
            cursor='hand2',
            relief='flat',
            padx=20,
            pady=10,
            command=self.show_system_info
        )
        sysinfo_btn.pack(fill='x', pady=5)

        # Exit button
        exit_btn = tk.Button(
            parent,
            text="🚪 Keluar",
            font=('Arial', 11),
            bg=DANGER_COLOR,
            fg='white',
            cursor='hand2',
            relief='flat',
            padx=20,
            pady=10,
            command=self.exit_app
        )
        exit_btn.pack(fill='x', pady=5)

    def create_upload_section(self, parent):
        """Create upload section"""
        upload_frame = tk.Frame(parent, bg='white')
        upload_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Model upload
        model_section = tk.LabelFrame(
            upload_frame,
            text="1. Upload Model YOLO (.pt)",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg=PRIMARY_COLOR,
            padx=20,
            pady=20
        )
        model_section.pack(fill='x', pady=(0, 20))

        self.model_label = tk.Label(
            model_section,
            text="Belum ada model dipilih",
            font=('Arial', 10),
            bg='white',
            fg='gray'
        )
        self.model_label.pack(pady=5)

        model_btn = tk.Button(
            model_section,
            text="📂 Pilih Model YOLO",
            font=('Arial', 11, 'bold'),
            bg=SECONDARY_COLOR,
            fg='white',
            cursor='hand2',
            relief='flat',
            padx=20,
            pady=10,
            command=self.upload_model
        )
        model_btn.pack()

        # Image upload
        image_section = tk.LabelFrame(
            upload_frame,
            text="2. Upload Images",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg=PRIMARY_COLOR,
            padx=20,
            pady=20
        )
        image_section.pack(fill='x', pady=(0, 20))

        self.image_label = tk.Label(
            image_section,
            text="Belum ada gambar dipilih",
            font=('Arial', 10),
            bg='white',
            fg='gray'
        )
        self.image_label.pack(pady=5)

        image_btn = tk.Button(
            image_section,
            text="📷 Pilih Gambar",
            font=('Arial', 11, 'bold'),
            bg=SECONDARY_COLOR,
            fg='white',
            cursor='hand2',
            relief='flat',
            padx=20,
            pady=10,
            command=self.upload_images
        )
        image_btn.pack()

        # Confidence threshold
        conf_section = tk.LabelFrame(
            upload_frame,
            text="3. Confidence Threshold",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg=PRIMARY_COLOR,
            padx=20,
            pady=20
        )
        conf_section.pack(fill='x', pady=(0, 20))

        conf_display = tk.Label(
            conf_section,
            textvariable=self.confidence,
            font=('Arial', 14, 'bold'),
            bg='white',
            fg=SUCCESS_COLOR
        )
        conf_display.pack(pady=5)

        conf_scale = tk.Scale(
            conf_section,
            from_=MIN_CONFIDENCE,
            to=MAX_CONFIDENCE,
            resolution=0.05,
            orient='horizontal',
            variable=self.confidence,
            bg='white',
            font=('Arial', 10),
            length=300
        )
        conf_scale.pack()

        # Analyze button
        analyze_btn = tk.Button(
            upload_frame,
            text="🔍 ANALYZE IMAGES",
            font=('Arial', 14, 'bold'),
            bg=SUCCESS_COLOR,
            fg='white',
            cursor='hand2',
            relief='flat',
            padx=40,
            pady=20,
            command=self.analyze_images
        )
        analyze_btn.pack(pady=20)

    def upload_model(self):
        """Upload YOLO model"""
        file_path = filedialog.askopenfilename(
            title="Pilih Model YOLO",
            filetypes=[("PyTorch Model", "*.pt"), ("All Files", "*.*")]
        )

        if file_path:
            self.model_path = file_path
            filename = os.path.basename(file_path)
            self.model_label.config(text=f"✅ Model: {filename}", fg=SUCCESS_COLOR)

    def upload_images(self):
        """Upload images"""
        mode = self.analysis_mode.get()

        if mode == "single":
            file_path = filedialog.askopenfilename(
                title="Pilih Gambar",
                filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp"), ("All Files", "*.*")]
            )
            if file_path:
                self.selected_images = [file_path]
                filename = os.path.basename(file_path)
                self.image_label.config(text=f"✅ Gambar: {filename}", fg=SUCCESS_COLOR)
        else:
            file_paths = filedialog.askopenfilenames(
                title="Pilih Gambar (Multiple)",
                filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp"), ("All Files", "*.*")]
            )
            if file_paths:
                self.selected_images = list(file_paths)
                count = len(file_paths)
                self.image_label.config(text=f"✅ {count} gambar dipilih", fg=SUCCESS_COLOR)

    def analyze_images(self):
        """Start image analysis"""
        # Validation
        if not self.model_path:
            messagebox.showerror("Error", "Silakan upload model YOLO terlebih dahulu!")
            return

        if not self.selected_images:
            messagebox.showerror("Error", "Silakan pilih gambar terlebih dahulu!")
            return

        # Set analysis data
        self.app_controller.set_analysis_data(
            model_path=self.model_path,
            image_paths=self.selected_images,
            confidence=self.confidence.get()
        )

        # Pindah ke dashboard 3
        self.app_controller.show_dashboard(3)

    def show_system_info(self):
        """Show system information"""
        info = f"""
SYSTEM INFORMATION

Aplikasi: Analisis Postur YOLO
Versi: 1.0.0
Python: 3.x
Framework: Tkinter

Dependencies:
- OpenCV
- Ultralytics YOLO
- Pillow
- Pandas
- NumPy

© 2024 Aplikasi Analisis Postur
        """
        messagebox.showinfo("System Info", info)

    def exit_app(self):
        """Exit aplikasi"""
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin keluar?"):
            self.parent.quit()
