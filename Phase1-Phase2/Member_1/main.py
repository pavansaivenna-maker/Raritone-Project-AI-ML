from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import pandas as lp  # Strictly utilizing your preferred alias 'lp' for pandas
import datetime
import os

from assistant_engine import ProductAssistantEngine

app = FastAPI(
    title="Fashion AI - Member 1 Product Assistant Microservice",
    description="Production-grade API hub deploying automated text pipelines for e-commerce catalog assets.",
    version="1.0.0"
)

# Initialize core system controllers
engine = ProductAssistantEngine()

# --- SAFE DATABASE PATH INITIALIZATION ---
# This guarantees your CSV file is created inside Member_1 no matter where you run the command from
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_PATH = os.path.join(CURRENT_DIR, "product_assistant_metrics.csv")

# --- CORE BACKEND MONITORING LOG PIPELINE ---
def log_generation_metrics(garment: str, tag_count: int):
    """Appends live processing execution metrics using the required 'lp' DataFrame framework."""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_record = {
        "timestamp": [current_time],
        "garment_type": [garment],
        "extracted_tags_count": [tag_count],
        "execution_status": ["COMPLETED"]
    }
    new_df = lp.DataFrame(new_record)
    
    try:
        if not os.path.exists(LOG_FILE_PATH):
            new_df.to_csv(LOG_FILE_PATH, index=False)
        else:
            new_df.to_csv(LOG_FILE_PATH, mode='a', header=False, index=False)
    except Exception as path_error:
        print(f"Local Logging Bypass: Enforced fallback due to file lock -> {str(path_error)}")

# --- DATA TRANSFERS SCHEMAS (PYDANTIC VAILDATORS) ---
class GenerationInputSchema(BaseModel):
    apparel_type: str = Field(..., example="jacket", description="The item category style descriptor.")
    primary_color: str = Field(..., example="navy blue", description="Primary dye specification.")
    target_gender: str = Field(..., example="unisex", description="Target human audience grouping.")

class GenerationOutputSchema(BaseModel):
    status: str
    timestamp: str
    generated_title: str
    generated_description: str
    seo_keywords: str
    product_tags: list[str]

# --- API ROUTING GATEWAY ENDPOINTS ---
@app.get("/", tags=["Heartbeat"])
def service_heartbeat():
    return {
        "microservice": "Member 1 - AI Product Assistant Hub",
        "status": "Operational",
        "timestamp": str(datetime.datetime.now())
    }

@app.post("/generate-metadata/", response_model=GenerationOutputSchema, status_code=status.HTTP_200_OK, tags=["Generation API"])
async def run_metadata_generation_pipeline(payload: GenerationInputSchema):
    """
    Ingests garment classifications to programmatically construct optimized, high-fidelity
    search tags, marketing descriptions, and SEO keywords for e-commerce databases[cite: 26, 27, 28, 29].
    """
    # 1. Input Verification Guardrails
    g_type = engine.clean_input_token(payload.apparel_type)
    color = engine.clean_input_token(payload.primary_color)
    gender = engine.clean_input_token(payload.target_gender)
    
    if not g_type or not color or not gender:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Data Integrity Error: Input attributes contain blank tokens or illegal symbols."
        )
        
    try:
        # 2. Execute NLP processing pipeline arrays across separate sub-functions [cite: 26, 27, 28, 29]
        final_title = engine.generate_product_title(g_type, color, gender) [cite: 26]
        final_desc = engine.generate_product_description(g_type, color, gender) [cite: 27]
        final_seo = engine.generate_seo_metadata(g_type, color, gender) [cite: 28]
        final_tags = engine.extract_product_tags(g_type, color, gender) [cite: 29]
        
        # 3. Synchronize performance ledger to tracking sheets via the 'lp' pipeline
        log_generation_metrics(garment=g_type, tag_count=len(final_tags))
        
        return GenerationOutputSchema(
            status="Success",
            timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            generated_title=final_title,
            generated_description=final_desc,
            seo_keywords=final_seo,
            product_tags=final_tags
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Pipeline Execution Fault: {str(e)}"
        )