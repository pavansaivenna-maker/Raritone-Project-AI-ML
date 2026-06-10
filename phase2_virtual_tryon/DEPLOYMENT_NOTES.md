# Deployment Guide: Try-On & Analytics

## 1. Environment Setup
Ensure Python 3.8+ is installed. Create a virtual environment and install the required dependencies:
`pip install rembg Pillow torchvision numpy fastapi uvicorn pydantic requests`

## 2. Running the Analytics Server
The FastAPI server must be running continuously to catch events from the frontend and other modules.
* **Command:** `python analytics_api.py`
* **Local Host:** Runs on `http://0.0.0.0:8000`
* **API Documentation:** Interactive Swagger UI is auto-generated at `http://127.0.0.1:8000/docs`

## 3. Running the Segmentation Engine
* **Command:** `python segmentation.py`
* **Note:** On the very first execution, the script will automatically download the required U^2-Net pre-trained weights. Ensure an active internet connection for the first run.