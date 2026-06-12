# config.py
import os

# Operational Computer Vision Thresholds
BLUR_THRESHOLD = 110.0       # Variance of Laplacian limit (lower indicates blur)
MIN_BRIGHTNESS = 45.0        # Minimum average luminance (0-255 scaling)
MAX_BRIGHTNESS = 235.0       # Maximum average luminance (0-255 scaling)
MIN_RESOLUTION = (600, 600)  # Width x Height micro-limit for stable segmentation

# Deep Learning Configurations (YOLOv8 Nano for production-speed throughput)
YOLO_MODEL_NAME = "yolov8n.pt"
CONFIDENCE_THRESHOLD = 0.50

# Valid COCO Class IDs related to fashion environments (Person, Backpack, Handbag, Tie)
VALID_FASHION_CLASSES = [0, 24, 26, 27]