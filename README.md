# DeepGuard - Deepfake Detection System

A complete end-to-end Deepfake Detection web application built with a FastAPI backend (PyTorch) and a React + TailwindCSS frontend. It uses a Hybrid CNN + Transformer (EfficientNetV2) architecture to identify visual manipulation artifacts.

## Folder Structure

- `src/` - Contains the PyTorch model definition (`model.py`).
- `backend/` - FastAPI backend application.
- `frontend/` - React frontend application.
- `real/` and `fake/` - Dataset directories for training.
- `test_model.py` - Script to verify the model architecture.

## Setup & Installation

### 1. Backend Setup

Open a terminal and navigate to the project root:

```bash
# Optional: Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install backend dependencies
pip install -r backend/requirements.txt
```

### 2. Frontend Setup

Open another terminal and navigate to the `frontend/` directory:

```bash
cd frontend
npm install
```

## Running the Application

### Start the Backend (FastAPI)

```bash
# Make sure you are in the project root
python backend/main.py
```
The API will run on `http://localhost:8000`. It will auto-create the SQLite database for prediction history.

### Start the Frontend (React + Vite)

```bash
# Make sure you are in the frontend/ directory
npm run dev
```
The UI will run on `http://localhost:5173`. Open this URL in your browser.

## Features

- **Inference**: Upload an image or video to the `/` route to get a real-time prediction.
- **Explainability (Grad-CAM)**: View the regions the model focused on to make its prediction for images.
- **Dashboard**: Navigate to `/dashboard` to view model evaluation metrics, trigger a live training run via SSE streaming, and view the history of all past predictions.

## Notes

- Make sure to place your real images inside `real/` and fake images inside `fake/` before initiating a training run from the Dashboard.
- The `src/model.py` MUST contain the `HybridDeepfakeDetector` class for the backend to run properly.