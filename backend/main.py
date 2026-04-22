from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import io
import torch
import sys
import os
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.model import HybridDeepfakeDetector

from backend.database import init_db, save_prediction, get_all_predictions
from backend.predict import predict_single_frame, predict_video
from backend.evaluate import evaluate_model
from backend.train import train_model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instance
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = None

@app.on_event("startup")
async def startup_event():
    await init_db()
    
    global model
    model = HybridDeepfakeDetector(cnn_model_name='efficientnetv2_rw_s', num_classes=1)
    
    best_model_path = os.path.join(os.path.dirname(__file__), 'weights', 'best_model.pth')
    if os.path.exists(best_model_path):
        model.load_state_dict(torch.load(best_model_path, map_location=device))
        print("Loaded pre-trained weights.")
    else:
        print("No pre-trained weights found. Using initialized model.")
        
    model.to(device)
    model.eval()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    
    # Check if video
    is_video = file.filename.lower().endswith(('.mp4', '.avi', '.mov'))
    
    try:
        if is_video:
            result = predict_video(model, contents, device)
        else:
            image = Image.open(io.BytesIO(contents)).convert("RGB")
            label, confidence, grad_cam_b64, prob = predict_single_frame(model, image, device)
            result = {
                "label": label,
                "confidence": float(confidence),
                "grad_cam_image": grad_cam_b64
            }
            
        # Save to DB
        await save_prediction(
            filename=file.filename,
            label=result["label"],
            confidence=result["confidence"],
            grad_cam_path=None # We store base64 in frontend, not db to save space
        )
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        # e.g., No face detected from preprocess.py will raise HTTPException
        raise e

from pydantic import BaseModel
class TrainParams(BaseModel):
    epochs: int
    batch_size: int
    learning_rate: float

@app.post("/train")
async def train(params: TrainParams):
    return StreamingResponse(
        train_model(params.epochs, params.batch_size, params.learning_rate),
        media_type="text/event-stream"
    )

@app.get("/evaluate")
async def evaluate():
    metrics = evaluate_model()
    if "error" in metrics:
        raise HTTPException(status_code=400, detail=metrics["error"])
    return metrics

@app.get("/history")
async def history():
    return await get_all_predictions()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
