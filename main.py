"""
Main Application - Entry Point
Aplikasi GUI Analisis Postur Menggunakan YOLO

Author: Posture Analysis System
Version: 1.0.0
"""
import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.config import *
from src.gui.dashboard_1 import Dashboard1
from src.gui.dashboard_2 import Dashboard2
from src.gui.dashboard_3 import Dashboard3
from src.gui.dashboard_4 import Dashboard4


class PostureAnalysisApp:
    """Main Application Controller"""

    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=BG_COLOR)

        # Center window
        self.center_window()

        # Data storage
        self.user_data = {
            'name': None,
            'height': None
        }

        self.analysis_data = {
            'model_path': None,
            'image_paths': [],
            'confidence': DEFAULT_CONFIDENCE
        }

        self.results_data = []

        # Current dashboard
        self.current_dashboard = None

        # Show first dashboard
        self.show_dashboard(1)

    def center_window(self):
        """Center window pada screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def show_dashboard(self, dashboard_number):
        """
        Show dashboard berdasarkan nomor

        Args:
            dashboard_number (int): Nomor dashboard (1-4)
        """
        # Destroy current dashboard
        if self.current_dashboard:
            self.current_dashboard.destroy()

        # Create new dashboard
        if dashboard_number == 1:
            self.current_dashboard = Dashboard1(self.root, self)
        elif dashboard_number == 2:
            self.current_dashboard = Dashboard2(self.root, self)
        elif dashboard_number == 3:
            self.current_dashboard = Dashboard3(self.root, self)
        elif dashboard_number == 4:
            self.current_dashboard = Dashboard4(self.root, self)
        else:
            messagebox.showerror("Error", f"Dashboard {dashboard_number} tidak ditemukan!")
            return

        self.current_dashboard.pack(fill='both', expand=True)

    def set_user_data(self, name, height):
        """
        Set user data

        Args:
            name (str): Nama user
            height (float): Tinggi badan dalam mm
        """
        self.user_data['name'] = name
        self.user_data['height'] = height

    def get_user_data(self):
        """
        Get user data

        Returns:
            dict: User data
        """
        return self.user_data

    def set_analysis_data(self, model_path, image_paths, confidence):
        """
        Set analysis data

        Args:
            model_path (str): Path ke model YOLO
            image_paths (list): List path ke images
            confidence (float): Confidence threshold
        """
        self.analysis_data['model_path'] = model_path
        self.analysis_data['image_paths'] = image_paths
        self.analysis_data['confidence'] = confidence

    def get_analysis_data(self):
        """
        Get analysis data

        Returns:
            dict: Analysis data
        """
        return self.analysis_data

    def set_results_data(self, results):
        """
        Set results data

        Args:
            results (list): List of analysis results
        """
        self.results_data = results

    def get_results_data(self):
        """
        Get results data

        Returns:
            list: Results data
        """
        return self.results_data


def main():
    """Main function"""
    try:
        # Create root window
        root = tk.Tk()

        # Create app
        app = PostureAnalysisApp(root)

        # Start mainloop
        root.mainloop()

    except Exception as e:
        messagebox.showerror("Fatal Error", f"Error starting application:\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
