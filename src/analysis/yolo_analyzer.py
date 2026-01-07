"""
YOLO Analyzer - Wrapper untuk YOLO model inference
"""
import cv2
import numpy as np
from ultralytics import YOLO
import time


class YOLOAnalyzer:
    """YOLO Model Analyzer untuk deteksi postur"""

    def __init__(self, model_path=None, confidence=0.25):
        """
        Initialize YOLO Analyzer

        Args:
            model_path (str): Path ke model YOLO .pt
            confidence (float): Confidence threshold
        """
        self.model_path = model_path
        self.confidence = confidence
        self.model = None

        if model_path:
            self.load_model(model_path)

    def load_model(self, model_path):
        """
        Load YOLO model

        Args:
            model_path (str): Path ke model .pt
        """
        try:
            self.model = YOLO(model_path)
            self.model_path = model_path
            print(f"✅ Model loaded: {model_path}")
        except Exception as e:
            raise Exception(f"❌ Error loading model: {str(e)}")

    def predict(self, image_path):
        """
        Run prediction pada image

        Args:
            image_path (str): Path ke image

        Returns:
            dict: Hasil prediksi dengan deteksi dan keypoints
        """
        if not self.model:
            raise Exception("❌ Model belum di-load!")

        start_time = time.time()

        # Run inference
        results = self.model.predict(
            source=image_path,
            conf=self.confidence,
            save=False,
            verbose=False
        )

        elapsed_time = time.time() - start_time

        # Parse results
        detections = self._parse_results(results)

        return {
            'detections': detections,
            'elapsed_time': elapsed_time,
            'image_path': image_path
        }

    def _parse_results(self, results):
        """
        Parse YOLO results

        Args:
            results: YOLO results object

        Returns:
            list: List of detections
        """
        detections = []

        for result in results:
            boxes = result.boxes
            keypoints = result.keypoints if hasattr(result, 'keypoints') else None

            for i in range(len(boxes)):
                detection = {
                    'class_id': int(boxes.cls[i]),
                    'class_name': result.names[int(boxes.cls[i])],
                    'confidence': float(boxes.conf[i]),
                    'bbox': boxes.xyxy[i].cpu().numpy().tolist(),
                    'keypoints': None
                }

                # Extract keypoints if available
                if keypoints is not None and len(keypoints) > i:
                    kp_data = keypoints[i].data.cpu().numpy()
                    if len(kp_data.shape) == 2:
                        detection['keypoints'] = kp_data[0].tolist()
                    else:
                        detection['keypoints'] = kp_data.tolist()

                detections.append(detection)

        return detections

    def annotate_image(self, image, detections):
        """
        Annotate image dengan deteksi dan keypoints

        Args:
            image (numpy.ndarray): Original image
            detections (list): List of detections

        Returns:
            numpy.ndarray: Annotated image
        """
        annotated = image.copy()

        for det in detections:
            # Draw bounding box
            bbox = det['bbox']
            x1, y1, x2, y2 = map(int, bbox)

            # Color based on class
            color = self._get_color_for_class(det['class_name'])

            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)

            # Draw label
            label = f"{det['class_name']} {det['confidence']:.2%}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.6
            thickness = 2

            (text_width, text_height), _ = cv2.getTextSize(label, font, font_scale, thickness)
            cv2.rectangle(annotated, (x1, y1 - text_height - 10),
                         (x1 + text_width + 10, y1), color, -1)
            cv2.putText(annotated, label, (x1 + 5, y1 - 5),
                       font, font_scale, (255, 255, 255), thickness)

            # Draw keypoints if available
            if det['keypoints']:
                annotated = self._draw_keypoints(annotated, det['keypoints'])

        return annotated

    def _draw_keypoints(self, image, keypoints):
        """
        Draw keypoints pada image

        Args:
            image (numpy.ndarray): Image
            keypoints (list): List of keypoints

        Returns:
            numpy.ndarray: Image dengan keypoints
        """
        # Reshape keypoints if needed
        if len(keypoints) % 3 == 0:
            num_points = len(keypoints) // 3
            keypoints = np.array(keypoints).reshape(num_points, 3)

        for kp in keypoints:
            if len(kp) >= 2:
                x, y = int(kp[0]), int(kp[1])
                conf = kp[2] if len(kp) > 2 else 1.0

                if conf > 0.1:
                    # Draw circle
                    cv2.circle(image, (x, y), 5, (255, 0, 0), -1)
                    cv2.circle(image, (x, y), 7, (0, 0, 0), 2)

        return image

    def _get_color_for_class(self, class_name):
        """
        Get color berdasarkan class name

        Args:
            class_name (str): Nama class

        Returns:
            tuple: RGB color
        """
        if 'Normal' in class_name:
            return (0, 255, 0)  # Green
        elif 'Kyphosis' in class_name:
            return (255, 0, 0)  # Red
        elif 'Lordosis' in class_name:
            return (255, 165, 0)  # Orange
        elif 'Swayback' in class_name:
            return (255, 255, 0)  # Yellow
        else:
            return (128, 128, 128)  # Gray

    def set_confidence(self, confidence):
        """
        Set confidence threshold

        Args:
            confidence (float): New confidence threshold
        """
        self.confidence = confidence
