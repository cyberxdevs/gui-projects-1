"""
Posture Analyzer - Analisis postur dari keypoints
"""
import numpy as np
import math
from config.config import POSTURE_MAPPING, ANALYSIS_TYPE_MAPPING, KEYPOINT_NAMES, KEYPOINT_EMOJIS, get_confidence_level


class PostureAnalyzer:
    """Analyzer untuk analisis postur dari deteksi YOLO"""

    def __init__(self, height_mm=1700):
        """
        Initialize Posture Analyzer

        Args:
            height_mm (float): Tinggi orang dalam mm
        """
        self.height_mm = height_mm

    def analyze(self, detections):
        """
        Analyze deteksi untuk mendapatkan imbalance

        Args:
            detections (list): List deteksi dari YOLO

        Returns:
            dict: Hasil analisis lengkap
        """
        if not detections:
            return {
                'success': False,
                'message': 'Tidak ada deteksi'
            }

        # Aggregate semua deteksi
        results = {
            'detections': [],
            'classifications': {},
            'imbalance': {},
            'score': 0,
            'analysis_type': None,
            'total_detections': len(detections)
        }

        for i, det in enumerate(detections):
            # Parse detection
            class_name = det['class_name']
            confidence = det['confidence']
            bbox = det['bbox']
            keypoints = det['keypoints']

            # Get classification
            classification = POSTURE_MAPPING.get(class_name, class_name)

            # Get analysis type
            subcategory = class_name.split('-')[-1] if '-' in class_name else ''
            analysis_type = ANALYSIS_TYPE_MAPPING.get(subcategory, 'back_front_analysis')

            if results['analysis_type'] is None:
                results['analysis_type'] = analysis_type

            # Count classifications
            if classification not in results['classifications']:
                results['classifications'][classification] = 0
            results['classifications'][classification] += 1

            # Calculate bbox properties
            x1, y1, x2, y2 = bbox
            width = x2 - x1
            height = x2 - y1
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            area = width * height

            detection_info = {
                'index': i + 1,
                'class': class_name,
                'classification': classification,
                'subcategory': class_name,
                'analysis_type': analysis_type,
                'confidence': confidence,
                'confidence_level': get_confidence_level(confidence),
                'bbox': bbox,
                'width': width,
                'height': height,
                'center': (center_x, center_y),
                'area': area,
                'keypoints': keypoints
            }

            results['detections'].append(detection_info)

            # Analyze keypoints if available
            if keypoints:
                imbalance = self._analyze_keypoints(keypoints, analysis_type, height)
                if imbalance:
                    # Merge imbalance results
                    for key, value in imbalance.items():
                        if key not in results['imbalance']:
                            results['imbalance'][key] = value

        # Calculate overall score
        results['score'] = self._calculate_score(results['imbalance'])

        return results

    def _analyze_keypoints(self, keypoints, analysis_type, bbox_height):
        """
        Analyze keypoints untuk mendapatkan imbalance

        Args:
            keypoints (list): List of keypoints
            analysis_type (str): Type of analysis
            bbox_height (float): Height of bounding box

        Returns:
            dict: Imbalance measurements
        """
        # Reshape keypoints
        if len(keypoints) % 3 == 0:
            num_points = len(keypoints) // 3
            kp_array = np.array(keypoints).reshape(num_points, 3)
        else:
            return {}

        # Calculate ratio (mm per pixel)
        ratio_mm_per_px = self.height_mm / max(bbox_height, 1)

        imbalance = {}

        if analysis_type == 'back_front_analysis':
            # Analyze for back/front view
            imbalance = self._analyze_back_front(kp_array, ratio_mm_per_px)
        elif analysis_type == 'side_analysis':
            # Analyze for side view
            imbalance = self._analyze_side(kp_array, ratio_mm_per_px)

        return imbalance

    def _analyze_back_front(self, keypoints, ratio):
        """
        Analyze untuk back/front view

        Args:
            keypoints (numpy.ndarray): Keypoints array
            ratio (float): mm per pixel ratio

        Returns:
            dict: Imbalance measurements
        """
        imbalance = {}

        # Shoulder imbalance
        if len(keypoints) >= 7:
            left_shoulder = keypoints[5]  # index 5
            right_shoulder = keypoints[6]  # index 6

            if left_shoulder[2] > 0.1 and right_shoulder[2] > 0.1:
                shoulder_diff_px = abs(left_shoulder[1] - right_shoulder[1])
                shoulder_diff_mm = shoulder_diff_px * ratio

                # Apply realistic limit
                if shoulder_diff_mm > 200:
                    shoulder_diff_mm = min(shoulder_diff_mm * 0.1, 50)

                imbalance['shoulder'] = shoulder_diff_mm

        # Hip imbalance
        if len(keypoints) >= 13:
            left_hip = keypoints[11]  # index 11
            right_hip = keypoints[12]  # index 12

            if left_hip[2] > 0.1 and right_hip[2] > 0.1:
                hip_diff_px = abs(left_hip[1] - right_hip[1])
                hip_diff_mm = hip_diff_px * ratio

                # Apply realistic limit
                if hip_diff_mm > 200:
                    hip_diff_mm = min(hip_diff_mm * 0.1, 50)

                imbalance['hip'] = hip_diff_mm

        # Spine deviation (simplified)
        if len(keypoints) >= 13:
            shoulders_available = keypoints[5][2] > 0.1 and keypoints[6][2] > 0.1
            hips_available = keypoints[11][2] > 0.1 and keypoints[12][2] > 0.1

            if shoulders_available and hips_available:
                shoulder_mid_x = (keypoints[5][0] + keypoints[6][0]) / 2
                hip_mid_x = (keypoints[11][0] + keypoints[12][0]) / 2

                spine_diff_px = abs(shoulder_mid_x - hip_mid_x)
                spine_diff_mm = spine_diff_px * ratio

                # Apply realistic limit
                if spine_diff_mm > 100:
                    spine_diff_mm = min(spine_diff_mm * 0.15, 30)

                imbalance['spine'] = spine_diff_mm

        return imbalance

    def _analyze_side(self, keypoints, ratio):
        """
        Analyze untuk side view

        Args:
            keypoints (numpy.ndarray): Keypoints array
            ratio (float): mm per pixel ratio

        Returns:
            dict: Imbalance measurements
        """
        imbalance = {}

        # Head shift (forward head posture)
        if len(keypoints) >= 7:
            nose = keypoints[0]  # index 0
            shoulders_available = keypoints[5][2] > 0.1 and keypoints[6][2] > 0.1

            if nose[2] > 0.1 and shoulders_available:
                shoulder_mid_x = (keypoints[5][0] + keypoints[6][0]) / 2
                head_shift_px = abs(nose[0] - shoulder_mid_x)
                head_shift_mm = head_shift_px * ratio

                # Apply realistic limit and auto-debug
                if head_shift_mm > 150:
                    head_shift_mm = min(head_shift_mm * 0.2, 40)
                elif head_shift_mm > 100:
                    head_shift_mm = min(head_shift_mm * 0.3, 35)

                imbalance['head_shift'] = head_shift_mm

        # Head tilt
        if len(keypoints) >= 5:
            left_eye = keypoints[1]  # index 1
            right_eye = keypoints[2]  # index 2

            if left_eye[2] > 0.1 and right_eye[2] > 0.1:
                dx = right_eye[0] - left_eye[0]
                dy = right_eye[1] - left_eye[1]
                angle = abs(math.degrees(math.atan2(dy, dx)))

                # Normalize angle
                if angle > 90:
                    angle = 180 - angle

                # Apply realistic limit
                if angle > 45:
                    angle = min(angle * 0.5, 30)

                imbalance['head_tilt'] = angle

        return imbalance

    def _calculate_score(self, imbalance):
        """
        Calculate overall score dari imbalance

        Args:
            imbalance (dict): Dictionary of imbalance measurements

        Returns:
            float: Score dari 0-100
        """
        if not imbalance:
            return 0

        total_score = 0
        count = 0

        # Score untuk setiap komponen
        for key, value in imbalance.items():
            if key in ['shoulder', 'hip', 'spine', 'head_shift']:
                # Linear scoring: 0mm = 100, 50mm = 0
                score = max(0, 100 - (value * 2))
            elif key == 'head_tilt':
                # Angular scoring: 0° = 100, 30° = 0
                score = max(0, 100 - (value * 3.33))
            else:
                score = 0

            total_score += score
            count += 1

        return total_score / count if count > 0 else 0

    def generate_report_text(self, results):
        """
        Generate report text dari hasil analisis

        Args:
            results (dict): Hasil analisis

        Returns:
            str: Report text
        """
        report = []

        # Header
        report.append("="*60)
        report.append("📊 DETEKSI DAN KLASIFIKASI POSTURAL")
        report.append("="*60)
        report.append("")

        # Deteksi
        for det in results['detections']:
            emoji = "🔸" if det['index'] % 2 == 1 else "🔹"
            report.append(f"{emoji} Deteksi {det['index']}:")
            report.append(f"   🦴 Kelas: {det['class']}")
            report.append(f"   🏷️  Klasifikasi: {det['classification']}")
            report.append(f"   📌 Sub-kategori: {det['subcategory']}")
            report.append(f"   🎯 Jenis Analisis: {det['analysis_type']}")
            report.append(f"   🎯 Confidence: {det['confidence']:.4f} ({det['confidence']*100:.1f}%)")
            report.append(f"   📊 Klasifikasi Confidence: {det['confidence_level']}")

            bbox = det['bbox']
            report.append(f"   📍 Bounding Box: [{bbox[0]:.1f}, {bbox[1]:.1f}, {bbox[2]:.1f}, {bbox[3]:.1f}]")
            report.append(f"   📏 Lebar: {det['width']:.1f}px")
            report.append(f"   📐 Tinggi: {det['height']:.1f}px")
            report.append(f"   🎯 Center: ({det['center'][0]:.1f}, {det['center'][1]:.1f})")
            report.append(f"   📊 Area: {det['area']:.1f}px²")
            report.append("")

            # Keypoints
            if det['keypoints']:
                report.append("  🔹 KEYPOINT DETECTION:")
                keypoints = det['keypoints']

                if len(keypoints) % 3 == 0:
                    num_points = len(keypoints) // 3
                    kp_array = np.array(keypoints).reshape(num_points, 3)

                    for i, kp in enumerate(kp_array):
                        if i < len(KEYPOINT_NAMES):
                            name = KEYPOINT_NAMES[i]
                            emoji = KEYPOINT_EMOJIS.get(name, '🔸')

                            if kp[2] > 0.05:
                                report.append(f"     {emoji} {name}: ({kp[0]:.1f}, {kp[1]:.1f}) - Confidence: {kp[2]:.2f} ({get_confidence_level(kp[2])})")

                report.append("")

        report.append(f"TOTAL DETEKSI: {results['total_detections']} objek/keypoint")
        report.append("="*60)
        report.append("")

        # Statistik
        report.append("📊 STATISTIK KLASIFIKASI:")
        for classification, count in results['classifications'].items():
            percentage = (count / results['total_detections']) * 100
            emoji = "🦴" if classification != 'Normal' else "✅"
            report.append(f"   {emoji} {classification}: {count} deteksi ({percentage:.1f}%)")
        report.append("")

        # Imbalance
        if results['imbalance']:
            report.append("📊 ANALISIS POSTUR BERDASARKAN KEYPOINT")
            report.append("="*50)
            report.append(f"📋 Jenis Analisis: {results['analysis_type']}")
            report.append("")

            imb = results['imbalance']
            if 'shoulder' in imb:
                report.append(f"   👤 Shoulder Imbalance: {imb['shoulder']:.1f} mm")
            if 'hip' in imb:
                report.append(f"   🏋️  Hip Imbalance: {imb['hip']:.1f} mm")
            if 'spine' in imb:
                report.append(f"   🦴 Spine Deviation: {imb['spine']:.1f} mm")
            if 'head_shift' in imb:
                report.append(f"   📏 Head Shift: {imb['head_shift']:.1f} mm")
            if 'head_tilt' in imb:
                report.append(f"   📐 Head Tilt: {imb['head_tilt']:.1f}°")

            report.append(f"   🏆 Overall Score: {results['score']:.1f}/100")
            report.append("")

        return "\n".join(report)

    def generate_classification_summary(self, results):
        """
        Generate classification summary

        Args:
            results (dict): Hasil analisis

        Returns:
            str: Summary text
        """
        summary = []

        summary.append("HASIL KLASIFIKASI POSTURAL:")

        for classification, count in results['classifications'].items():
            if classification != 'Normal':
                emoji = "🦴"
                summary.append(f"{emoji} {classification}: {count} deteksi")

        if not any(c != 'Normal' for c in results['classifications'].keys()):
            summary.append("✅ Postur Normal - Tidak ada kelainan terdeteksi")

        summary.append("")
        summary.append("💡 REKOMENDASI BERDASARKAN ANALISIS:")

        score = results['score']
        if score >= 80:
            summary.append("    Postur baik. Pertahankan dan lakukan peregangan rutin.")
        elif score >= 60:
            summary.append("    Postur cukup baik. Perhatikan posisi duduk dan berdiri.")
        elif score >= 40:
            summary.append("    Postur perlu perbaikan. Konsultasi dengan fisioterapis direkomendasikan.")
        elif score >= 20:
            summary.append("    Postur buruk. Segera konsultasi dengan spesialis.")
        else:
            summary.append("    Postur kritis. Segera konsultasi dengan spesialis.")

        return "\n".join(summary)
