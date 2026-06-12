# validation_engine.py
import cv2
import numpy as np
from ultralytics import YOLO
import config

class GarmentValidationEngine:
    def __init__(self):
        # Load model globally on startup to prevent memory leaks and API latency
        self.detector = YOLO(config.YOLO_MODEL_NAME)

    def evaluate_image_quality(self, image: np.ndarray) -> dict:
        """Runs pixel-level checks to identify focus blur, improper lighting, or small resolutions."""
        h, w, _ = image.shape
        gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 1. Focus evaluation via Variance of Laplacian Operator
        blur_score = cv2.Laplacian(gray_frame, cv2.CV_64F).var()
        is_blurry = bool(blur_score < config.BLUR_THRESHOLD) # Added bool()
        
        # 2. Exposure evaluation via Mean Luminance values
        mean_luminance = np.mean(gray_frame)
        is_poor_exposure = bool((mean_luminance < config.MIN_BRIGHTNESS) or (mean_luminance > config.MAX_BRIGHTNESS)) # Added bool()
        
        # 3. Resolution edge constraint evaluation
        is_low_res = bool((w < config.MIN_RESOLUTION[0]) or (h < config.MIN_RESOLUTION[1])) # Added bool()
        
        passed_quality = bool(not (is_blurry or is_poor_exposure or is_low_res)) # Added bool()
        
        return {
            "passed_quality_gate": passed_quality,
            "metrics": {
                "blur_variance": float(round(blur_score, 2)),
                "mean_luminance": float(round(mean_luminance, 2)),
                "dimensions": f"{w}x{h}"
            },
            "failures": {
                "blurry_artifact": is_blurry,
                "exposure_malformed": is_poor_exposure,
                "insufficient_resolution": is_low_res
            }
        }

    def detect_garment_anchors(self, image: np.ndarray) -> list:
        """Parses the frame to find valid target objects before allowing virtual try-on processing."""
        # Scale input sizes to 640px to protect pipeline throughput speeds
        inference_results = self.detector(image, imgsz=640, verbose=False)[0]
        
        extracted_anchors = []
        for box in inference_results.boxes:
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            
            if confidence >= config.CONFIDENCE_THRESHOLD and class_id in config.VALID_FASHION_CLASSES:
                label = self.detector.names[class_id]
                coordinates = box.xyxy[0].tolist()
                
                extracted_anchors.append({
                    "detected_class": label,
                    "confidence_score": float(round(confidence, 3)),
                    "bounding_box_xyxy": [int(pixel) for pixel in coordinates]
                })
        return extracted_anchors