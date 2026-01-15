# streamlit_app.py
import streamlit as st
import requests
from PIL import Image
import io
import base64
import os
from utils.base_utils import load_env_variables

# ------------------------------
# Configuration
# ------------------------------
# FastAPI endpoint
load_env_variables()
API_URL = os.getenv("API_URL")

st.title("🍎 Food Spoilage Detector")
st.write("Upload an image of food and get instant spoilage prediction!")

CLASS_EMOJIS = {
    0: "🍎 Fresh Apple",      
    1: "🤢 Rotten Apple",    
}

# ------------------------------
# Upload Section
# ------------------------------
uploaded_file = st.file_uploader("Upload an image of food", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width="content")
    st.write("")


    if st.button("Predict Spoilage"):
        with st.spinner("Analyzing..."):
            try:

                # Convert image to base64
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")   

                # Send POST request to FastAPI
                response = requests.post(API_URL, json={"image": img_str}, timeout=30)
                result = response.json()

                prediction = result[0]
                class_idx = CLASS_EMOJIS.get(prediction["class_index"], "Unknown")
                confidence = prediction["confidence"] * 100
                st.write("")

                # Display result
                if "error" in result:
                    st.error(f"Error: {result['error']}")
                else:
                    st.success(f"Prediction Result: {class_idx} with {confidence:.2f}% confidence")
                    st.write(result)

            except Exception as e:
                st.error(f"Failed to get prediction: {e}")
