# main.py
import time
import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from validation_engine import GarmentValidationEngine
import analytics_logger

app = FastAPI(
    title="Garment Detection & Validation API",
    description="Production microservice for Phase 2 image vetting and structural validation.",
    version="1.0.0"
)

# Instantiate engine into active memory
engine = GarmentValidationEngine()

@app.post("/api/v1/validate-product-image", status_code=status.HTTP_200_OK)
async def process_product_validation(image_file: UploadFile = File(...)):
    """
    Evaluates image quality metrics and object anchors dynamically.
    """
    start_timestamp = time.time()
    filename_lower = image_file.filename.lower()
    
    if not filename_lower.endswith(('.jpg', '.jpeg', '.png', '.webp')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported media encoding. Must be standard web image array."
        )
    
    try:
        # Stream raw binary directly into memory buffers (compatible with Backend team dynamic datasets)
        binary_buffer = await image_file.read()
        numpy_array = np.frombuffer(binary_buffer, np.uint8)
        decoded_image = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)
        
        if decoded_image is None:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Corrupted image matrix.")
        
        # 1. Product Image Validation (OpenCV)
        quality_audit = engine.evaluate_image_quality(decoded_image)
        
        # 2. Garment Detection Model (YOLOv8)
        detected_objects = []
        if quality_audit["passed_quality_gate"]:
            detected_objects = engine.detect_garment_anchors(decoded_image)
            
        has_valid_anchor = len(detected_objects) > 0
        is_pipeline_approved = quality_audit["passed_quality_gate"] and has_valid_anchor
        
        execution_latency = time.time() - start_timestamp
        verdict_status = "APPROVED" if is_pipeline_approved else "REJECTED"
        
        # 3. Performance Optimization Logging
        analytics_logger.commit_pipeline_log(
            filename=image_file.filename,
            processing_time=execution_latency,
            quality_ok=quality_audit["passed_quality_gate"],
            anchor_ok=has_valid_anchor,
            metrics=quality_audit["metrics"]
        )
        
        # Structured return payload
        return {
            "pipeline_summary": {
                "file_name": image_file.filename,
                "overall_verdict": verdict_status,
                "latency_sec": round(execution_latency, 4)
            },
            "quality_validation": quality_audit,
            "garment_detection": {
                "anchor_found": has_valid_anchor,
                "match_count": len(detected_objects),
                "matches": detected_objects
            }
        }
        
    except Exception as internal_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Validation Core Failure: {str(internal_error)}"
        )