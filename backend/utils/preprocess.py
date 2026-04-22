import torch
from torchvision import transforms
from facenet_pytorch import MTCNN
from PIL import Image
from fastapi import HTTPException

# Initialize MTCNN for face detection
# margin=20 adds some context around the face, post_process=False keeps values [0, 255]
mtcnn = MTCNN(image_size=224, margin=20, keep_all=False, post_process=False)

# ImageNet normalization standard
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])

def preprocess_image(image: Image.Image) -> torch.Tensor:
    """
    Detects face, crops, resizes to 224x224, and normalizes it.
    Input: PIL Image (RGB)
    Output: torch.Tensor of shape [1, 3, 224, 224]
    """
    # MTCNN returns a cropped and resized face tensor of shape [3, 224, 224] if a face is found.
    # The values are un-normalized [0, 255] because post_process=False.
    face_tensor = mtcnn(image)
    
    if face_tensor is None:
        raise HTTPException(status_code=422, detail="No face detected in image")
    
    # Scale to [0, 1]
    face_tensor = face_tensor / 255.0
    
    # Normalize using ImageNet stats
    face_tensor = normalize(face_tensor)
    
    # Add batch dimension [1, 3, 224, 224]
    return face_tensor.unsqueeze(0)
