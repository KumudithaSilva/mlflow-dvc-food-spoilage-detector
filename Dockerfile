# ========================
# Base image
# ========================
FROM python:3.10-slim

# ========================
# Environment variables
# ========================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

# ========================
# Set working directory
# ========================
WORKDIR /app

# ========================
# Install dependencies
# ========================
COPY requirement.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirement.txt

# ========================
# Copy only necessary files for prediction
# ========================
COPY src/ ./src/
COPY config/ ./config/
COPY params.yaml ./params.yaml
COPY template/ ./template/
COPY app.py ./app.py
COPY .env ./  

# ========================
# Expose ports
# ========================
EXPOSE 8000   
EXPOSE 8501  

# ========================
# Run FastAPI and Streamlit together
# ========================
CMD ["bash", "-c", "\
    uvicorn app:app --host 0.0.0.0 --port 8000 & \
    streamlit run template/streamlit_app.py --server.port 8501 --server.address 0.0.0.0 \
"]
