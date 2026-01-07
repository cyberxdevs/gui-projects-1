"""
Image Utilities - Image Processing Helper Functions
"""
import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk


def load_image(image_path):
    """
    Load image dari path

    Args:
        image_path (str): Path ke file gambar

    Returns:
        numpy.ndarray: Image array
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Tidak dapat membaca gambar: {image_path}")
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def resize_image_for_display(img, max_width=800, max_height=600):
    """
    Resize image untuk display di GUI

    Args:
        img (numpy.ndarray): Image array
        max_width (int): Maximum width
        max_height (int): Maximum height

    Returns:
        numpy.ndarray: Resized image
    """
    height, width = img.shape[:2]

    # Calculate scale
    scale_w = max_width / width
    scale_h = max_height / height
    scale = min(scale_w, scale_h, 1.0)  # Don't upscale

    if scale < 1.0:
        new_width = int(width * scale)
        new_height = int(height * scale)
        img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

    return img


def numpy_to_photoimage(img):
    """
    Convert numpy array ke PhotoImage untuk Tkinter

    Args:
        img (numpy.ndarray): Image array (RGB)

    Returns:
        ImageTk.PhotoImage: PhotoImage object
    """
    if img.dtype != np.uint8:
        img = img.astype(np.uint8)

    pil_img = Image.fromarray(img)
    return ImageTk.PhotoImage(pil_img)


def draw_bounding_box(img, bbox, label, confidence, color=(0, 255, 0)):
    """
    Draw bounding box pada image

    Args:
        img (numpy.ndarray): Image array
        bbox (list): [x1, y1, x2, y2]
        label (str): Label text
        confidence (float): Confidence score
        color (tuple): RGB color

    Returns:
        numpy.ndarray: Image dengan bounding box
    """
    img_copy = img.copy()
    x1, y1, x2, y2 = map(int, bbox)

    # Draw rectangle
    cv2.rectangle(img_copy, (x1, y1), (x2, y2), color, 2)

    # Draw label background
    label_text = f"{label} {confidence:.2%}"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    thickness = 2
    (text_width, text_height), _ = cv2.getTextSize(label_text, font, font_scale, thickness)

    cv2.rectangle(img_copy, (x1, y1 - text_height - 10), (x1 + text_width + 10, y1), color, -1)
    cv2.putText(img_copy, label_text, (x1 + 5, y1 - 5), font, font_scale, (255, 255, 255), thickness)

    return img_copy


def draw_keypoints(img, keypoints, keypoint_names, color=(255, 0, 0)):
    """
    Draw keypoints pada image

    Args:
        img (numpy.ndarray): Image array
        keypoints (list): List of keypoints [[x, y, conf], ...]
        keypoint_names (list): List of keypoint names
        color (tuple): RGB color

    Returns:
        numpy.ndarray: Image dengan keypoints
    """
    img_copy = img.copy()

    for i, (kp, name) in enumerate(zip(keypoints, keypoint_names)):
        if len(kp) >= 2:
            x, y = int(kp[0]), int(kp[1])
            conf = kp[2] if len(kp) > 2 else 1.0

            if conf > 0.1:  # Only draw if confidence > 0.1
                # Draw circle
                cv2.circle(img_copy, (x, y), 5, color, -1)
                cv2.circle(img_copy, (x, y), 7, (0, 0, 0), 2)

                # Draw label
                cv2.putText(img_copy, name, (x + 10, y), cv2.FONT_HERSHEY_SIMPLEX,
                           0.4, (255, 255, 255), 2)
                cv2.putText(img_copy, name, (x + 10, y), cv2.FONT_HERSHEY_SIMPLEX,
                           0.4, color, 1)

    return img_copy


def create_side_by_side_image(img1, img2, label1="Before", label2="After"):
    """
    Create side by side image comparison

    Args:
        img1 (numpy.ndarray): First image
        img2 (numpy.ndarray): Second image
        label1 (str): Label for first image
        label2 (str): Label for second image

    Returns:
        numpy.ndarray: Combined image
    """
    # Resize to same height
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]

    target_height = min(h1, h2)
    img1 = cv2.resize(img1, (int(w1 * target_height / h1), target_height))
    img2 = cv2.resize(img2, (int(w2 * target_height / h2), target_height))

    # Add labels
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img1, label1, (10, 30), font, 1, (255, 255, 255), 3)
    cv2.putText(img1, label1, (10, 30), font, 1, (0, 0, 0), 2)
    cv2.putText(img2, label2, (10, 30), font, 1, (255, 255, 255), 3)
    cv2.putText(img2, label2, (10, 30), font, 1, (0, 255, 0), 2)

    # Combine horizontally
    combined = np.hstack([img1, img2])

    return combined
