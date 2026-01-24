import base64
import os
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient
from PIL import Image

from app import app

# ---------------------------
# Setup Test Client
# ---------------------------
# FastAPI TestClient allows us to simulate API calls without running a server
client = TestClient(app)

# ---------------------------
# Ensure upload directory exists
# ---------------------------
UPLOAD_DIR = Path(os.getenv("OBJECT_STORE_ROOT", "temp"))
UPLOAD_DIR.mkdir(exist_ok=True)


@patch("app.prediction_pipeline.main")  # Mock prediction
@patch("app.s3_client.upload_fileobj")  # Mock S3 upload
def test_predict_endpoint(mock_s3_upload, mock_predict):
    """
    Test the /api/predict endpoint with a dummy in-memory image.
    Steps:
    1. Create a dummy image in memory.
    2. Encode it to base64 (as required by the endpoint).
    3. Call the /api/predict endpoint.
    4. Check status code and response structure.
    5. Verify S3 upload was attempted.
    """

    # ---------------------------
    # Create a dummy model output
    # ---------------------------
    mock_predict.return_value = [
        {"class_index": 0, "confidence": 0.99, "image": "dummy.png"}
    ]

    # ---------------------------
    # Create a dummy image in memory
    # ---------------------------
    dummy_img = Image.new("RGB", (10, 10), color=(255, 0, 0))
    img_bytes_io = BytesIO()
    dummy_img.save(img_bytes_io, format="PNG")
    img_bytes_io.seek(0)

    # ---------------------------
    # Encode image to base64
    # ---------------------------
    img_b64 = base64.b64encode(img_bytes_io.read()).decode("utf-8")

    # ---------------------------
    # Call the /api/predict endpoint
    # ---------------------------
    response = client.post("/api/predict", json={"image": img_b64})

    # ---------------------------
    # Basic response check
    # ---------------------------
    assert response.status_code == 200

    # Convert JSON response to Python object
    result = response.json()

    # ---------------------------
    # Check response structure
    # ---------------------------
    # The prediction pipeline returns a list of dictionaries

    assert isinstance(result, list)
    assert len(result) > 0

    first_item = result[0]
    expected_keys = {"class_index", "confidence", "image"}
    assert expected_keys.issubset(first_item.keys())

    # ---------------------------
    # Ensure S3 upload was called
    # ---------------------------
    mock_s3_upload.assert_called()
