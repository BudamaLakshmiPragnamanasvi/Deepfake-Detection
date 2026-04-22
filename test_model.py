import sys
import os
import torch

from src.model import HybridDeepfakeDetector

def test_model_architecture():
    print("Initializing Hybrid CNN + Transformer Model (EfficientNetV2)...")
    try:
        model = HybridDeepfakeDetector(cnn_model_name='efficientnetv2_rw_s', num_classes=1)
        model.eval()
        
        # Create a dummy batch of 2 images [BatchSize, Channels, Height, Width]
        print("Creating dummy tensor of shape [2, 3, 224, 224]...")
        dummy_input = torch.randn(2, 3, 224, 224)
        
        # Forward pass
        with torch.no_grad():
            output = model(dummy_input)
            
        print(f"Forward pass successful! Output shape: {output.shape}")
        
        if output.shape == (2, 1):
            print("SUCCESS: Model architecture is correctly built and passes dummy tensor test.")
        else:
            print(f"WARNING: Unexpected output shape. Expected (2, 1), got {output.shape}")
            
    except Exception as e:
        print(f"FAILED: An error occurred during model testing:\n{e}")

if __name__ == "__main__":
    test_model_architecture()
