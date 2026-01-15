from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from pipeline.stage_06_prediction import PredictionPipeline
from utils.image_utils import decodeImage
import traceback
import os 
import uuid


# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

OBJECT_STORE_ROOT = Path(os.getenv("OBJECT_STORE_ROOT", "object_store"))
UPLOAD_DIR = OBJECT_STORE_ROOT / "prediction_data"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# FastAPI App
# ------------------------------------------------------------

app = FastAPI(title="Food Spoilage Detector")

# Allow CORS for Streamlit requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------
# Load Prediction Pipeline ONCE
# ------------------------------------------------------------

prediction_pipeline = PredictionPipeline()


# ------------------------------------------------------------
# Request Schema
# ------------------------------------------------------------

class ImageRequest(BaseModel):
    image: str


# ------------------------------------------------------------
# Prediction Endpoint
# ------------------------------------------------------------

@app.post("/predict")
def predict(data: ImageRequest):
    """
    1. Generate unique object key
    2. Save image to object storage
    3. Pass path to prediction pipeline
    """
    try:
        # Generate unique object name
        image_name = f"{uuid.uuid4()}.png"
        image_path = UPLOAD_DIR / image_name
        
        # decode base64
        decodeImage(data.image, image_path)

        # run prediction
        result = prediction_pipeline.run([image_path])

        return result
    
    except Exception as e:
        traceback.print_exc()
        
        return {"error": str(e)}







