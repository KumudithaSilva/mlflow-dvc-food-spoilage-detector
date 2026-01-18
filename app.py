from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from pipeline.stage_07_prediction import PredictionPipeline
from utils.image_utils import decodeImageToPNGBytes, saveBytesToFile
import traceback
import os 
import uuid
from utils.s3_utils import S3Client


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
# Temporally File location
# ------------------------------------------------------------

UPLOAD_DIR = Path(os.getenv("OBJECT_STORE_ROOT", "temp"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# S3 Config
# ------------------------------------------------------------

S3_BUCKET = os.getenv("S3_BUCKET", "food-spoilage-ml")
S3_BUCKET_DIR = os.getenv("S3_BUCKET_DIR", "user-uploads")
s3_client = S3Client() 

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
    2. Save image to object storage and S3
    3. Pass path to prediction pipeline
    """
    try:
        # Generate unique object name
        image_name = f"{uuid.uuid4()}.png"

        image_path = UPLOAD_DIR / image_name
        s3_key = f"{S3_BUCKET_DIR}/{image_name}"
        
        # Decode base64
        file_obj = decodeImageToPNGBytes(data.image)

        # Writes a BytesIO object to given path
        saveBytesToFile(file_obj, image_path)

        # Upload to S3
        s3_client.upload_fileobj(file_obj, S3_BUCKET, s3_key)
    
        # run prediction
        result = prediction_pipeline.main([image_path])

        return result
    
    except Exception as e:
        traceback.print_exc()
        
        return {"error": str(e)}







