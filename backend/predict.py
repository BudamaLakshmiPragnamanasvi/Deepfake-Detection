import os
import io
import torch
import cv2
import numpy as np
from PIL import Image
from backend.utils.preprocess import preprocess_image
from backend.utils.grad_cam import generate_grad_cam_base64
import tempfile

def predict_single_frame(model, image: Image.Image, device):
    """
    Runs prediction on a single PIL image.
    Returns label ("Real" or "Fake"), confidence, and grad_cam base64 string.
    """
    input_tensor = preprocess_image(image).to(device)
    
    # Original image as numpy array for grad_cam
    orig_np = np.array(image.convert('RGB'))
    
    # Inference
    with torch.no_grad():
        output = model(input_tensor)
        prob = torch.sigmoid(output).item()
        
    confidence = prob if prob >= 0.5 else 1 - prob
    label = "Fake" if prob >= 0.5 else "Real"
    
    grad_cam_b64 = generate_grad_cam_base64(model, input_tensor, orig_np)
    
    return label, confidence, grad_cam_b64, prob

def predict_video(model, video_bytes: bytes, device):
    """
    Extracts 1 frame/sec from video and aggregates predictions.
    """
    # Write video bytes to temp file to read with cv2
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
        tmp_file.write(video_bytes)
        tmp_path = tmp_file.name
        
    cap = cv2.VideoCapture(tmp_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    if fps == 0:
        fps = 30 # fallback
        
    frame_results = []
    frame_probs = []
    
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Extract 1 frame per second
        if frame_count % fps == 0:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(frame_rgb)
            
            try:
                # We skip grad_cam for video frames to save computation, or we just keep the last one.
                # Let's keep grad_cam of the frame that is most "Fake"
                label, confidence, grad_cam, prob = predict_single_frame(model, pil_img, device)
                
                frame_results.append({
                    "frame_num": frame_count,
                    "label": label,
                    "confidence": float(confidence),
                    "grad_cam": grad_cam
                })
                frame_probs.append(prob)
            except Exception as e:
                # MTCNN might not detect a face in some frames
                pass
                
        frame_count += 1
        
    cap.release()
    os.remove(tmp_path)
    
    if not frame_results:
        raise ValueError("No faces detected in any video frames.")
        
    # Aggregate (Majority vote)
    avg_prob = sum(frame_probs) / len(frame_probs)
    final_label = "Fake" if avg_prob >= 0.5 else "Real"
    final_confidence = avg_prob if avg_prob >= 0.5 else 1 - avg_prob
    
    # Pick the grad cam of the frame with highest fake probability
    worst_frame = max(frame_results, key=lambda x: x["confidence"] if x["label"] == "Fake" else -x["confidence"])
    
    return {
        "label": final_label,
        "confidence": float(final_confidence),
        "grad_cam_image": worst_frame["grad_cam"],
        "frame_results": [{k: v for k, v in f.items() if k != "grad_cam"} for f in frame_results]
    }
