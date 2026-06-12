from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import pandas as lp  # Using preferred alias 'lp' for pandas
import datetime
import shutil
import uuid
import os
import io

# Import your core machine learning validation engine component
from validation_engine import GarmentValidationEngine

# ==========================================
# 📊 INTERNAL ANALYTICS LOGGER FUNCTIONALITY
# ==========================================
# 1. Ensure the dataset directory exists locally so the app doesn't crash
os.makedirs(os.path.join(os.path.dirname(__file__), "dataset"), exist_ok=True)

# 2. Sets the clean cross-platform path for your analytics file inside the folder
LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), "dataset", "garment_validation_analytics.csv")

def log_validation_metrics(filename: str, objects_detected: int, status: str):
    """
    Automated logging function that records AI validation metrics directly 
    into your CSV tracking database using your preferred 'lp' pandas pipeline.
    """
    # 1. Capture the exact timestamp of the evaluation check
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 2. Structure the new record row matrix
    new_data = {
        "timestamp": [current_time],
        "file_name": [filename],
        "garments_found": [objects_detected],
        "validation_status": [status]
    }
    
    # 3. Build a temporary DataFrame using the 'lp' alias
    new_df = lp.DataFrame(new_data)
    
    # 4. Append metrics safely to the dataset tracker sheet
    if not os.path.exists(LOG_FILE_PATH):
        new_df.to_csv(LOG_FILE_PATH, index=False)
    else:
        new_df.to_csv(LOG_FILE_PATH, mode='a', header=False, index=False)
        
    print(f"--> [LOG SUCCESS] Metrics appended to database sheet for: {filename}")


# ==========================================
# 🌐 FASTAPI APPLICATION ROUTING & ENGINE
# ==========================================
app = FastAPI(
    title="Fashion AI - Member 4 Unified Microservice",
    description="Production-grade API layer combining Object Detection, Quality Validation, and Ingestion Analytics.",
    version="1.0.0"
)

# Initialize your core validation engine safely (loads your yolov8n.pt weights)
try:
    engine = GarmentValidationEngine()
except Exception as e:
    print(f"CRITICAL: Failed to initialize GarmentValidationEngine: {str(e)}")
    engine = None

class ValidationSummaryResponse(BaseModel):
    status: str
    filename: str
    detected_objects_count: int
    validation_passed: bool
    remarks: str

# --- API ENDPOINTS ---

@app.get("/")
def read_root():
    """
    Heartbeat route to verify microservice health and model engine availability.
    """
    return {
        "service": "Member 4 - Unified Garment Detection & Validation Engine",
        "status": "Healthy",
        "model_loaded": engine is not None
    }

@app.post("/validate-image/", response_model=ValidationSummaryResponse)
async def validate_product_image(file: UploadFile = File(...)):
    """
    Accepts a raw product image upload, runs real-time YOLOv8 garment anchor detection,
    evaluates quality compliance thresholds, and records execution metrics.
    """
    # Image Format Guardrail
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        raise HTTPException(status_code=400, detail="Unsupported image format. Please upload PNG, JPG, or WEBP.")
        
    if engine is None:
        raise HTTPException(status_code=500, detail="Detection engine weights are currently unavailable.")

    try:
        # Secure a unique temporary file path for CV2 stream processing
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        unique_id = uuid.uuid4().hex
        temp_file_path = os.path.join(temp_dir, f"{unique_id}_{file.filename}")
        
        # Write uploaded bytes data stream to local drive
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Execute object prediction pipeline to fetch xyxy coordinates and classes
        anchors = engine.detect_garment_anchors(temp_file_path)
        
        detected_count = len(anchors)
        is_valid = detected_count > 0
        remarks = "Image passed verification standards." if is_valid else "Validation Failed: No garments detected."
        
        # Trigger internal logging function combined right inside this file
        log_validation_metrics(
            filename=file.filename,
            objects_detected=detected_count,
            status="PASSED" if is_valid else "FAILED"
        )
        
        # Clean up temporary disk file space
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            
        return ValidationSummaryResponse(
            status="Success",
            filename=file.filename,
            detected_objects_count=detected_count,
            validation_passed=is_valid,
            remarks=remarks
        )
        
    except Exception as e:
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=f"Internal Image Processing Error: {str(e)}")

@app.post("/upload-csv/")
async def upload_csv_analytics(file: UploadFile = File(...)):
    """
    Processes validation analytics logs matrices using the required 'lp' pandas dataframe pipeline.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid data file format. Only standard CSV tables supported.")
    
    try:
        contents = await file.read()
        data_buffer = io.BytesIO(contents)
        
        # Parsing data streams into structured dataframes using your 'lp' convention
        df = lp.read_csv(data_buffer)
        
        if df.empty:
            return {"status": "Empty File Passed", "records_processed": 0}
            
        return {
            "status": "Analytics Synchronized",
            "filename": file.filename,
            "records_processed": len(df),
            "schema_columns": list(df.columns),
            "preview": df.head(3).to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Stream Ingestion Error: {str(e)}")