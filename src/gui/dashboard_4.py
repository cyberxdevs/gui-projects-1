"""
Dashboard 4 - Results dan Export
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from PIL import Image, ImageTk
import os
from config.config import *
from src.utils.image_utils import resize_image_for_display, numpy_to_photoimage
from src.utils.export_utils import export_to_csv
from src.analysis.posture_analyzer import PostureAnalyzer


class Dashboard4(tk.Frame):
    """Dashboard keempat untuk menampilkan hasil dan export"""

    def __init__(self, parent, app_controller):
        super().__init__(parent, bg=BG_COLOR)
        self.parent = parent
        self.app_controller = app_controller

        self.results_data = app_controller.get_results_data()
        self.current_result_index = 0

        self.setup_ui()
        self.display_result(0)

    def setup_ui(self):
        """Setup UI components"""
        # Header
        header_frame = tk.Frame(self, bg=PRIMARY_COLOR)
        header_frame.pack(fill='x', pady=(0, 20))

        header_label = tk.Label(
            header_frame,
            text="HASIL ANALISIS POSTUR",
            font=('Arial', 24, 'bold'),
            bg=PRIMARY_COLOR,
            fg='white',
            pady=20
        )
        header_label.pack()

        # Main container with notebook (tabs)
        main_container = tk.Frame(self, bg=BG_COLOR)
        main_container.pack(expand=True, fill='both', padx=30, pady=20)

        # Create notebook
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(expand=True, fill='both')

        # Tab 1: Visualization
        viz_tab = tk.Frame(self.notebook, bg='white')
        self.notebook.add(viz_tab, text="📊 Visualization")

        self.create_visualization_tab(viz_tab)

        # Tab 2: Analysis Table
        table_tab = tk.Frame(self.notebook, bg='white')
        self.notebook.add(table_tab, text="📋 Analysis Table")

        self.create_table_tab(table_tab)

        # Tab 3: Summary Report
        summary_tab = tk.Frame(self.notebook, bg='white')
        self.notebook.add(summary_tab, text="📝 Summary")

        self.create_summary_tab(summary_tab)

        # Button panel
        button_panel = tk.Frame(main_container, bg=BG_COLOR)
        button_panel.pack(fill='x', pady=(20, 0))

        button_frame = tk.Frame(button_panel, bg=BG_COLOR)
        button_frame.pack()

        # Export CSV button
        export_btn = tk.Button(
            button_frame,
            text="💾 Export to CSV",
            font=('Arial', 12, 'bold'),
            bg=SECONDARY_COLOR,
            fg='white',
            cursor='hand2',
            relief='flat',
            padx=30,
            pady=12,
            command=self.export_csv
        )
        export_btn.pack(side='left', padx=10)

        # Back button
        back_btn = tk.Button(
            button_frame,
            text="🔙 Back to Upload",
            font=('Arial', 12, 'bold'),
            bg=WARNING_COLOR,
            fg='white',
            cursor='hand2',
            relief='flat',
            padx=30,
            pady=12,
            command=self.back_to_dashboard2
        )
        back_btn.pack(side='left', padx=10)

        # New analysis button
        new_btn = tk.Button(
            button_frame,
            text="🔄 New Analysis",
            font=('Arial', 12, 'bold'),
            bg=SUCCESS_COLOR,
            fg='white',
            cursor='hand2',
            relief='flat',
            padx=30,
            pady=12,
            command=self.new_analysis
        )
        new_btn.pack(side='left', padx=10)

    def create_visualization_tab(self, parent):
        """Create visualization tab"""
        # Image selector
        selector_frame = tk.Frame(parent, bg='white')
        selector_frame.pack(fill='x', padx=20, pady=10)

        tk.Label(
            selector_frame,
            text="Select Image:",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg=PRIMARY_COLOR
        ).pack(side='left', padx=(0, 10))

        self.image_selector = ttk.Combobox(
            selector_frame,
            font=('Arial', 11),
            state='readonly',
            width=50
        )
        self.image_selector.pack(side='left', padx=(0, 10))
        self.image_selector.bind('<<ComboboxSelected>>', self.on_image_selected)

        # Populate selector
        image_names = [f"Image {i+1}: {os.path.basename(r['image_path'])}"
                      for i, r in enumerate(self.results_data)]
        self.image_selector['values'] = image_names
        if image_names:
            self.image_selector.current(0)

        # Image display
        image_frame = tk.Frame(parent, bg='white', relief='sunken', borderwidth=2)
        image_frame.pack(fill='both', expand=True, padx=20, pady=10)

        self.viz_image_label = tk.Label(image_frame, bg='white')
        self.viz_image_label.pack(expand=True, pady=20)

        # Info text
        info_frame = tk.Frame(parent, bg='white')
        info_frame.pack(fill='x', padx=20, pady=10)

        self.viz_info_text = scrolledtext.ScrolledText(
            info_frame,
            font=('Courier', 9),
            bg='#f8f9fa',
            fg=PRIMARY_COLOR,
            height=10,
            wrap='word'
        )
        self.viz_info_text.pack(fill='both', expand=True)

    def create_table_tab(self, parent):
        """Create analysis table tab"""
        # Table frame
        table_frame = tk.Frame(parent, bg='white')
        table_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Table title
        title_label = tk.Label(
            table_frame,
            text="TABEL HASIL ANALISIS IMBALANCE POSTURAL",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg=PRIMARY_COLOR
        )
        title_label.pack(pady=(0, 10))

        # Create treeview
        columns = ('Komponen', 'Parameter', 'Nilai', 'Satuan', 'Status', 'Score')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)

        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center', width=120)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Populate table
        self.populate_table()

    def create_summary_tab(self, parent):
        """Create summary tab"""
        summary_frame = tk.Frame(parent, bg='white')
        summary_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Title
        title_label = tk.Label(
            summary_frame,
            text="RINGKASAN HASIL ANALISIS",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg=PRIMARY_COLOR
        )
        title_label.pack(pady=(0, 20))

        # Summary text
        self.summary_text = scrolledtext.ScrolledText(
            summary_frame,
            font=('Arial', 12),
            bg='#f8f9fa',
            fg=PRIMARY_COLOR,
            wrap='word'
        )
        self.summary_text.pack(fill='both', expand=True)

        # Populate summary
        self.populate_summary()

    def display_result(self, index):
        """Display result untuk index tertentu"""
        if index >= len(self.results_data):
            return

        result = self.results_data[index]
        self.current_result_index = index

        # Display annotated image
        annotated_img = result['annotated_img']
        display_img = resize_image_for_display(annotated_img, max_width=800, max_height=500)
        photo = numpy_to_photoimage(display_img)

        self.viz_image_label.config(image=photo)
        self.viz_image_label.image = photo

        # Display info
        self.viz_info_text.delete('1.0', 'end')
        self.viz_info_text.insert('1.0', result['report_text'])

    def on_image_selected(self, event):
        """Handle image selection"""
        index = self.image_selector.current()
        self.display_result(index)

    def populate_table(self):
        """Populate analysis table"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Aggregate all results
        if not self.results_data:
            return

        # Use first result for now (bisa dimodifikasi untuk aggregate)
        result = self.results_data[self.current_result_index]
        imbalance = result['posture_results'].get('imbalance', {})

        # Add rows
        from src.utils.export_utils import get_status, get_component_score

        if 'shoulder' in imbalance:
            self.tree.insert('', 'end', values=(
                'Shoulder Imbalance',
                'Perbedaan Tinggi Bahu',
                f"{imbalance['shoulder']:.1f}",
                'mm',
                get_status('shoulder', imbalance['shoulder']),
                get_component_score('shoulder', imbalance['shoulder'])
            ))

        if 'hip' in imbalance:
            self.tree.insert('', 'end', values=(
                'Hip Imbalance',
                'Perbedaan Tinggi Pinggul',
                f"{imbalance['hip']:.1f}",
                'mm',
                get_status('hip', imbalance['hip']),
                get_component_score('hip', imbalance['hip'])
            ))

        if 'spine' in imbalance:
            self.tree.insert('', 'end', values=(
                'Spine Imbalance',
                'Deviasi Tulang Belakang',
                f"{imbalance['spine']:.1f}",
                'mm',
                get_status('spine', imbalance['spine']),
                get_component_score('spine', imbalance['spine'])
            ))

        if 'head_shift' in imbalance:
            self.tree.insert('', 'end', values=(
                'Head Shift',
                'Pergeseran Kepala',
                f"{imbalance['head_shift']:.1f}",
                'mm',
                get_status('head_shift', imbalance['head_shift']),
                get_component_score('head_shift', imbalance['head_shift'])
            ))

        if 'head_tilt' in imbalance:
            self.tree.insert('', 'end', values=(
                'Head Tilt',
                'Kemiringan Kepala',
                f"{imbalance['head_tilt']:.1f}",
                '°',
                get_status('head_tilt', imbalance['head_tilt']),
                get_component_score('head_tilt', imbalance['head_tilt'])
            ))

        # Overall score
        overall_score = result['posture_results'].get('score', 0)
        from src.utils.export_utils import get_overall_status
        self.tree.insert('', 'end', values=(
            'OVERALL',
            'Total Score',
            f"{overall_score:.1f}",
            '/100',
            get_overall_status(overall_score),
            f"{overall_score:.1f}"
        ), tags=('overall',))

        # Style overall row
        self.tree.tag_configure('overall', background='#d5f4e6', font=('Arial', 10, 'bold'))

    def populate_summary(self):
        """Populate summary text"""
        self.summary_text.delete('1.0', 'end')

        # User info
        user_data = self.app_controller.get_user_data()
        self.summary_text.insert('end', "="*60 + "\n")
        self.summary_text.insert('end', "LAPORAN ANALISIS POSTUR TUBUH\n")
        self.summary_text.insert('end', "="*60 + "\n\n")

        self.summary_text.insert('end', f"Nama: {user_data['name']}\n")
        self.summary_text.insert('end', f"Tinggi Badan: {user_data['height']} mm ({user_data['height']/10} cm)\n")
        self.summary_text.insert('end', f"Jumlah Gambar Dianalisis: {len(self.results_data)}\n\n")

        # For each result, add summary
        for i, result in enumerate(self.results_data):
            self.summary_text.insert('end', f"\n{'='*60}\n")
            self.summary_text.insert('end', f"HASIL ANALISIS GAMBAR {i+1}\n")
            self.summary_text.insert('end', f"{'='*60}\n\n")

            posture_results = result['posture_results']
            analyzer = PostureAnalyzer(user_data['height'])
            summary = analyzer.generate_classification_summary(posture_results)

            self.summary_text.insert('end', summary)
            self.summary_text.insert('end', "\n\n")

        self.summary_text.insert('end', "\n" + "="*60 + "\n")
        self.summary_text.insert('end', "© 2024 Aplikasi Analisis Postur - Powered by YOLO\n")
        self.summary_text.insert('end', "="*60 + "\n")

    def export_csv(self):
        """Export hasil ke CSV"""
        try:
            user_data = self.app_controller.get_user_data()
            result = self.results_data[self.current_result_index]

            # Export
            filepath = export_to_csv(
                result['posture_results'],
                user_data['name'],
                EXPORTS_DIR
            )

            messagebox.showinfo(
                "Success",
                f"Data berhasil di-export ke:\n{filepath}"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Error saat export: {str(e)}")

    def back_to_dashboard2(self):
        """Kembali ke dashboard 2"""
        self.app_controller.show_dashboard(2)

    def new_analysis(self):
        """Mulai analisis baru"""
        if messagebox.askyesno("Konfirmasi", "Mulai analisis baru? Data saat ini akan hilang."):
            self.app_controller.show_dashboard(1)
