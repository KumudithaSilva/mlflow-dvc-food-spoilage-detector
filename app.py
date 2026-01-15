from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from pipeline.stage_06_prediction import PredictionPipeline
from utils.image_utils import decodeImage
import traceback

# FastAPI app
app = FastAPI(title="Food Spoilage Detector")

# Allow CORS for Streamlit requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Image storage path
TEMP_IMAGE_PATH = Path("prediction_data/inputImage.png")
# Load Model
pipeline = PredictionPipeline([TEMP_IMAGE_PATH])


# Request schema
class ImageRequest(BaseModel):
    image: str


@app.get("/")
def root():
    # Redirect user to Streamlit
    return RedirectResponse("http://localhost:8501")


@app.post("/predict")
def predict(data: ImageRequest):
    try:
        # decode base64
        decodeImage(data.image, TEMP_IMAGE_PATH)
        # update pipeline
        pipeline.image_paths = [TEMP_IMAGE_PATH]
        # run prediction
        result = pipeline.main()

        return result
    
    except Exception as e:
        traceback.print_exc()
        
        return {"error": str(e)}







