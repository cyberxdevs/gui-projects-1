"""
Dashboard 1 - Input Name dan Height
"""
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from config.config import *


class Dashboard1(tk.Frame):
    """Dashboard awal untuk input nama dan tinggi badan"""

    def __init__(self, parent, app_controller):
        super().__init__(parent, bg=BG_COLOR)
        self.parent = parent
        self.app_controller = app_controller

        self.setup_ui()

    def setup_ui(self):
        """Setup UI components"""
        # Main container
        main_container = tk.Frame(self, bg=BG_COLOR)
        main_container.pack(expand=True, fill='both', padx=50, pady=50)

        # Logo
        self.load_logo(main_container)

        # Title
        title_label = tk.Label(
            main_container,
            text="APLIKASI ANALISIS POSTUR",
            font=('Arial', 32, 'bold'),
            bg=BG_COLOR,
            fg=PRIMARY_COLOR
        )
        title_label.pack(pady=(20, 10))

        subtitle_label = tk.Label(
            main_container,
            text="Sistem Deteksi dan Analisis Postur Tubuh Menggunakan YOLO",
            font=('Arial', 14),
            bg=BG_COLOR,
            fg=SECONDARY_COLOR
        )
        subtitle_label.pack(pady=(0, 40))

        # Form Container
        form_frame = tk.Frame(main_container, bg='white', relief='raised', borderwidth=2)
        form_frame.pack(pady=20, padx=100, fill='x')

        # Form content
        form_content = tk.Frame(form_frame, bg='white')
        form_content.pack(padx=40, pady=40)

        # Name input
        name_label = tk.Label(
            form_content,
            text="Nama Lengkap:",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg=PRIMARY_COLOR
        )
        name_label.grid(row=0, column=0, sticky='w', pady=(0, 5))

        self.name_entry = tk.Entry(
            form_content,
            font=('Arial', 14),
            width=40,
            relief='solid',
            borderwidth=1
        )
        self.name_entry.grid(row=1, column=0, pady=(0, 30))

        # Height input
        height_label = tk.Label(
            form_content,
            text="Tinggi Badan (mm):",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg=PRIMARY_COLOR
        )
        height_label.grid(row=2, column=0, sticky='w', pady=(0, 5))

        height_frame = tk.Frame(form_content, bg='white')
        height_frame.grid(row=3, column=0, pady=(0, 20))

        self.height_entry = tk.Entry(
            height_frame,
            font=('Arial', 14),
            width=15,
            relief='solid',
            borderwidth=1
        )
        self.height_entry.pack(side='left', padx=(0, 10))

        height_info = tk.Label(
            height_frame,
            text="Contoh: 1700 (untuk 170 cm)",
            font=('Arial', 10, 'italic'),
            bg='white',
            fg='gray'
        )
        height_info.pack(side='left')

        # Submit button
        submit_btn = tk.Button(
            form_content,
            text="MULAI ANALISIS",
            font=('Arial', 14, 'bold'),
            bg=SUCCESS_COLOR,
            fg='white',
            padx=30,
            pady=15,
            cursor='hand2',
            relief='flat',
            command=self.submit_form
        )
        submit_btn.grid(row=4, column=0, pady=(20, 0))

        # Bind hover effects
        submit_btn.bind('<Enter>', lambda e: submit_btn.config(bg='#229954'))
        submit_btn.bind('<Leave>', lambda e: submit_btn.config(bg=SUCCESS_COLOR))

        # Footer
        footer_label = tk.Label(
            main_container,
            text="© 2024 Aplikasi Analisis Postur - Powered by YOLO",
            font=('Arial', 10),
            bg=BG_COLOR,
            fg='gray'
        )
        footer_label.pack(side='bottom', pady=20)

    def load_logo(self, parent):
        """Load dan tampilkan logo"""
        logo_frame = tk.Frame(parent, bg=BG_COLOR)
        logo_frame.pack(pady=(0, 20))

        try:
            if os.path.exists(LOGO_PATH):
                logo_img = Image.open(LOGO_PATH)
                logo_img = logo_img.resize((150, 150), Image.Resampling.LANCZOS)
                logo_photo = ImageTk.PhotoImage(logo_img)

                logo_label = tk.Label(logo_frame, image=logo_photo, bg=BG_COLOR)
                logo_label.image = logo_photo
                logo_label.pack()
            else:
                # Placeholder jika logo tidak ada
                placeholder = tk.Label(
                    logo_frame,
                    text="📊",
                    font=('Arial', 80),
                    bg=BG_COLOR
                )
                placeholder.pack()
        except Exception as e:
            print(f"Error loading logo: {e}")
            placeholder = tk.Label(
                logo_frame,
                text="📊",
                font=('Arial', 80),
                bg=BG_COLOR
            )
            placeholder.pack()

    def submit_form(self):
        """Handle form submission"""
        name = self.name_entry.get().strip()
        height_str = self.height_entry.get().strip()

        # Validation
        if not name:
            messagebox.showerror("Error", "Nama tidak boleh kosong!")
            return

        if not height_str:
            messagebox.showerror("Error", "Tinggi badan tidak boleh kosong!")
            return

        try:
            height = float(height_str)
            if height < 1000 or height > 2500:
                messagebox.showerror("Error", "Tinggi badan harus antara 1000-2500 mm (100-250 cm)!")
                return
        except ValueError:
            messagebox.showerror("Error", "Tinggi badan harus berupa angka!")
            return

        # Save data dan pindah ke dashboard 2
        self.app_controller.set_user_data(name, height)
        self.app_controller.show_dashboard(2)
