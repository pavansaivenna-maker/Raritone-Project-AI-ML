# Garment Detection & Automated Quality Validation Engine

## 📌 Microservice Overview
This repository contains the standalone AI validation microservice for **Member 4**. The system ingests raw fashion product imagery, performs localized object detection to extract garment anchors, enforces asset quality guardrails, and records structured execution analytics.

### Core Responsibilities
* **Garment Detection:** Localizing apparel assets using a pre-trained `yolov8n.pt` computer vision weight matrix.
* **Asset Quality Enforcement:** Bypassing malformed or low-confidence imagery to prevent pipeline crashes.
* **Analytics Ingestion:** Structuring execution logs into a localized metrics matrix via an optimized pandas pipeline.

---

## 🏗️ System Architecture & Data Flow
The microservice has been fully optimized to centralize data storage and telemetry logs into a unified directory structure:

```text
Member_4/
│
├── 📁 dataset/                             <-- Centralized Data Store
│   ├── garment_validation_analytics.csv    <-- Auto-generated AI Run Logs
│   └── [Backend Team Schema CSVs]          <-- Auth, Inventory, Products, etc.
│
├── 📄 main.py                              <-- FastAPI Application & Routing
├── 📄 validation_engine.py                 <-- YOLOv8 Core Detection Object
└── 📄 yolov8n.pt                           <-- Neural Network Weight Matrix

---

🚀 How to Run and Test the Microservice
Step 1: Initialize the Local API Server
Ensure your virtual environment is active, navigate to the directory, and boot up the FastAPI Uvicorn engine:

PowerShell
cd P:\AI_ML_Internship\Fashion-AI\Member_4
uvicorn main:app --reload --port 8000
Step 2: Access the Interactive Docs Layout
Open your web browser and navigate to:
👉 http://127.0.0.1:8000/docs

Step 3: Run the Ingestion & Analytics Tests
Expand the POST /validate-image/ route block.

Click "Try it out", upload a sample clothing image file, and press "Execute".

The system will process the image coordinates and instantly append the execution row matrix directly inside your local database path: dataset/garment_validation_analytics.csv.

## 🌐 API Specifications & Integration Mapping

### 1. Real-Time Image Validation
* **Endpoint:** `POST /validate-image/`
* **Content-Type:** `multipart/form-data`
* **Request Payload:** Raw Image Binary (`.jpg`, `.jpeg`, `.png`, `.webp`)

#### Expected Success Response (`200 OK`)
```json
{
  "status": "Success",
  "filename": "sample_shirt.jpg",
  "detected_objects_count": 1,
  "validation_passed": true,
  "remarks": "Image passed verification standards."
}
2. Analytics Ledger Sync
Endpoint: POST /upload-csv/

Request Payload: Multi-part CSV file tracking data metrics tables.

🛠️ Local Environment Execution Guide
Prerequisites
Ensure your terminal environment is running Python 3.11+ and has the core workspace dependencies installed (fastapi, uvicorn, ultralytics, pandas).

Running the Uvicorn Server
Step directly into the module workspace directory:

PowerShell
cd Member_4
Boot up the local development live-reload server:

PowerShell
uvicorn main:app --reload
Access the interactive API playground docs via your browser at: http://127.0.0.1:8000/docs