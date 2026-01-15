# streamlit_app.py
import streamlit as st
import requests
from PIL import Image
import io
import base64

# FastAPI endpoint
API_URL = "http://127.0.0.1:8000/predict"  # change if deployed elsewhere

st.title("🍎 Food Spoilage Detector")
st.write("")

CLASS_EMOJIS = {
    0: "🍎 Fresh Apple",      
    1: "🤢 Rotten Apple",    
}

# Upload image
uploaded_file = st.file_uploader("Upload an image of food", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width="content")
    st.write("")

    # Convert image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    if st.button("Predict Spoilage"):
        with st.spinner("Analyzing..."):
            try:
                # Send POST request to FastAPI
                response = requests.post(API_URL, json={"image": img_str})
                result = response.json()

                prediction = result[0]
                class_idx = prediction["class_index"]
                confidence = prediction.get("confidence", 0)

                label_emoji = CLASS_EMOJIS.get(class_idx)
                st.write("")

                # Display result
                if "error" in result:
                    st.error(f"Error: {result['error']}")
                else:
                    st.success(f"Prediction Result: {label_emoji} with {confidence*100}% Confidence")
                    st.write(result)

            except Exception as e:
                st.error(f"Failed to get prediction: {e}")
