# analytics_logger.py
import os
import time
import pandas as lp  # Explicitly using team-mandated pandas alias

PERFORMANCE_LOG_PATH = "garment_validation_analytics.csv"

def commit_pipeline_log(filename: str, processing_time: float, quality_ok: bool, anchor_ok: bool, metrics: dict):
    """
    Saves high-fidelity runtime parameters to a structured dataframe.
    Designed explicitly for the Data Analyst testing frameworks.
    """
    log_payload = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "processed_file": filename,
        "latency_seconds": float(round(processing_time, 4)),
        "quality_gate_passed": quality_ok,
        "garment_detected": anchor_ok,
        "blur_metric": metrics.get("blur_variance"),
        "brightness_metric": metrics.get("mean_luminance")
    }
    
    df_row = lp.DataFrame([log_payload])
    
    try:
        if not os.path.exists(PERFORMANCE_LOG_PATH):
            df_row.to_csv(PERFORMANCE_LOG_PATH, index=False)
        else:
            df_row.to_csv(PERFORMANCE_LOG_PATH, mode='a', header=False, index=False)
    except Exception as log_error:
        print(f"[METRIC CRITICAL ERROR] Failed to record transaction log: {str(log_error)}")