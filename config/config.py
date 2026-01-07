"""
Konfigurasi Aplikasi GUI Analisis Postur
"""
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
EXPORTS_DIR = os.path.join(BASE_DIR, 'exports')

# Ensure directories exist
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(EXPORTS_DIR, exist_ok=True)

# GUI Settings
WINDOW_TITLE = "Aplikasi Analisis Postur - YOLO"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
BG_COLOR = "#f0f0f0"
PRIMARY_COLOR = "#2c3e50"
SECONDARY_COLOR = "#3498db"
SUCCESS_COLOR = "#27ae60"
WARNING_COLOR = "#f39c12"
DANGER_COLOR = "#e74c3c"

# Logo Settings
LOGO_PATH = os.path.join(ASSETS_DIR, 'logo.png')

# YOLO Settings
DEFAULT_CONFIDENCE = 0.25
MIN_CONFIDENCE = 0.1
MAX_CONFIDENCE = 1.0

# Posture Classification Mapping
POSTURE_MAPPING = {
    'Normal-Kanan': 'Normal',
    'Normal-Kiri': 'Normal',
    'Normal-Belakang': 'Normal',
    'Normal-Depan': 'Normal',
    'Kyphosis-Kanan': 'Kyphosis',
    'Kyphosis-Kiri': 'Kyphosis',
    'Kyphosis-Belakang': 'Kyphosis',
    'Kyphosis-Depan': 'Kyphosis',
    'Lordosis-Kanan': 'Lordosis',
    'Lordosis-Kiri': 'Lordosis',
    'Lordosis-Belakang': 'Lordosis',
    'Lordosis-Depan': 'Lordosis',
    'Swayback-Kanan': 'Swayback',
    'Swayback-Kiri': 'Swayback',
    'Swayback-Belakang': 'Swayback',
    'Swayback-Depan': 'Swayback',
}

# Analysis Types
ANALYSIS_TYPE_MAPPING = {
    'Kanan': 'back_front_analysis',
    'Kiri': 'back_front_analysis',
    'Belakang': 'side_analysis',
    'Depan': 'side_analysis',
}

# Keypoint Names
KEYPOINT_NAMES = [
    'nose', 'left_eye', 'right_eye', 'left_ear', 'right_ear',
    'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow',
    'left_wrist', 'right_wrist', 'left_hip', 'right_hip',
    'left_knee', 'right_knee', 'left_ankle', 'right_ankle'
]

# Keypoint Emojis
KEYPOINT_EMOJIS = {
    'nose': '👃',
    'left_eye': '👁️',
    'right_eye': '👁️',
    'left_ear': '👂',
    'right_ear': '👂',
    'left_shoulder': '💪',
    'right_shoulder': '💪',
    'left_elbow': '🦾',
    'right_elbow': '🦾',
    'left_wrist': '🤲',
    'right_wrist': '🤲',
    'left_hip': '🦵',
    'right_hip': '🦵',
    'left_knee': '🦿',
    'right_knee': '🦿',
    'left_ankle': '🦶',
    'right_ankle': '🦶',
}

# Confidence Levels
def get_confidence_level(conf):
    """Get confidence level label"""
    if conf >= 0.9:
        return "Sangat Tinggi"
    elif conf >= 0.7:
        return "Tinggi"
    elif conf >= 0.5:
        return "Sedang"
    elif conf >= 0.3:
        return "Rendah"
    else:
        return "Sangat Rendah"
