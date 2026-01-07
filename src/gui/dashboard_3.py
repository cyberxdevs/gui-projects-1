"""
Dashboard 3 - Visualization Before/After dengan Analisis
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
import cv2
import numpy as np
import threading
from config.config import *
from src.analysis.yolo_analyzer import YOLOAnalyzer
from src.analysis.posture_analyzer import PostureAnalyzer
from src.utils.image_utils import load_image, resize_image_for_display, numpy_to_photoimage, create_side_by_side_image


class Dashboard3(tk.Frame):
    """Dashboard ketiga untuk visualisasi before/after analisis"""

    def __init__(self, parent, app_controller):
        super().__init__(parent, bg=BG_COLOR)
        self.parent = parent
        self.app_controller = app_controller

        self.yolo_analyzer = None
        self.posture_analyzer = None
        self.analysis_results = []
        self.current_image_index = 0

        self.setup_ui()
        self.start_analysis()

    def setup_ui(self):
        """Setup UI components"""
        # Header
        header_frame = tk.Frame(self, bg=PRIMARY_COLOR)
        header_frame.pack(fill='x', pady=(0, 20))

        header_label = tk.Label(
            header_frame,
            text="VISUALISASI ANALISIS POSTUR",
            font=('Arial', 24, 'bold'),
            bg=PRIMARY_COLOR,
            fg='white',
            pady=20
        )
        header_label.pack()

        # Main container
        main_container = tk.Frame(self, bg=BG_COLOR)
        main_container.pack(expand=True, fill='both', padx=30, pady=20)

        # Image display frame
        image_frame = tk.Frame(main_container, bg='white', relief='raised', borderwidth=2)
        image_frame.pack(fill='both', expand=True, pady=(0, 20))

        # Loading label
        self.loading_label = tk.Label(
            image_frame,
            text="⏳ Sedang menganalisis gambar...\nMohon tunggu...",
            font=('Arial', 16),
            bg='white',
            fg=PRIMARY_COLOR
        )
        self.loading_label.pack(expand=True, pady=100)

        # Image canvas
        self.image_canvas = tk.Canvas(image_frame, bg='white', highlightthickness=0)
        self.image_label = tk.Label(self.image_canvas, bg='white')

        # Scrollbar untuk canvas
        scrollbar_y = tk.Scrollbar(image_frame, orient='vertical', command=self.image_canvas.yview)
        scrollbar_x = tk.Scrollbar(image_frame, orient='horizontal', command=self.image_canvas.xview)

        self.image_canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Info panel
        info_panel = tk.Frame(main_container, bg='white', relief='raised', borderwidth=2)
        info_panel.pack(fill='x', pady=(0, 20))

        self.info_text = scrolledtext.ScrolledText(
            info_panel,
            font=('Courier', 10),
            bg='white',
            fg=PRIMARY_COLOR,
            height=8,
            wrap='word'
        )
        self.info_text.pack(fill='both', expand=True, padx=10, pady=10)

        # Button panel
        button_panel = tk.Frame(main_container, bg=BG_COLOR)
        button_panel.pack(fill='x')

        self.results_btn = tk.Button(
            button_panel,
            text="📊 VIEW RESULTS",
            font=('Arial', 14, 'bold'),
            bg=SUCCESS_COLOR,
            fg='white',
            cursor='hand2',
            relief='flat',
            padx=40,
            pady=15,
            command=self.show_results,
            state='disabled'
        )
        self.results_btn.pack()

    def start_analysis(self):
        """Start analysis dalam thread terpisah"""
        thread = threading.Thread(target=self.run_analysis, daemon=True)
        thread.start()

    def run_analysis(self):
        """Run YOLO analysis"""
        try:
            # Get data
            analysis_data = self.app_controller.get_analysis_data()
            user_data = self.app_controller.get_user_data()

            model_path = analysis_data['model_path']
            image_paths = analysis_data['image_paths']
            confidence = analysis_data['confidence']
            height_mm = user_data['height']

            # Initialize analyzers
            self.yolo_analyzer = YOLOAnalyzer(model_path, confidence)
            self.posture_analyzer = PostureAnalyzer(height_mm)

            # Analyze images
            for img_path in image_paths:
                self.update_loading(f"Menganalisis: {img_path}")

                # Run YOLO prediction
                yolo_results = self.yolo_analyzer.predict(img_path)

                # Analyze posture
                posture_results = self.posture_analyzer.analyze(yolo_results['detections'])

                # Load images
                original_img = load_image(img_path)
                annotated_img = self.yolo_analyzer.annotate_image(original_img, yolo_results['detections'])

                # Create side-by-side
                combined_img = create_side_by_side_image(
                    original_img,
                    annotated_img,
                    label1="BEFORE",
                    label2="AFTER ANALYSIS"
                )

                # Generate report
                report_text = self.posture_analyzer.generate_report_text(posture_results)

                # Store results
                result = {
                    'image_path': img_path,
                    'yolo_results': yolo_results,
                    'posture_results': posture_results,
                    'original_img': original_img,
                    'annotated_img': annotated_img,
                    'combined_img': combined_img,
                    'report_text': report_text
                }

                self.analysis_results.append(result)

            # Display first result
            if self.analysis_results:
                self.display_result(0)
                self.parent.after(0, lambda: self.results_btn.config(state='normal'))

        except Exception as e:
            error_msg = f"Error during analysis: {str(e)}"
            print(error_msg)
            self.parent.after(0, lambda: messagebox.showerror("Error", error_msg))

    def update_loading(self, message):
        """Update loading message"""
        self.parent.after(0, lambda: self.loading_label.config(text=f"⏳ {message}"))

    def display_result(self, index):
        """Display analysis result"""
        if index >= len(self.analysis_results):
            return

        result = self.analysis_results[index]
        self.current_image_index = index

        # Hide loading
        self.loading_label.pack_forget()

        # Display combined image
        combined_img = result['combined_img']
        display_img = resize_image_for_display(combined_img, max_width=1000, max_height=500)
        photo = numpy_to_photoimage(display_img)

        self.image_label.config(image=photo)
        self.image_label.image = photo

        # Pack canvas components
        self.image_canvas.pack(fill='both', expand=True, padx=10, pady=10)
        self.image_canvas.create_window(0, 0, window=self.image_label, anchor='nw')
        self.image_canvas.config(scrollregion=self.image_canvas.bbox('all'))

        # Display report
        self.info_text.delete('1.0', 'end')
        self.info_text.insert('1.0', result['report_text'])

    def show_results(self):
        """Show results dashboard"""
        if self.analysis_results:
            # Save results to app controller
            self.app_controller.set_results_data(self.analysis_results)

            # Navigate to dashboard 4
            self.app_controller.show_dashboard(4)
