import torch
import torch.nn as nn
import timm

class HybridDeepfakeDetector(nn.Module):
    def __init__(self, cnn_model_name='efficientnetv2_rw_s', num_classes=1):
        super(HybridDeepfakeDetector, self).__init__()
        # Mock efficientnetv2 backbone
        self.backbone = timm.create_model(cnn_model_name, pretrained=True, num_classes=0)
        self.fc = nn.Linear(self.backbone.num_features, num_classes)
        
    def forward(self, x):
        features = self.backbone(x)
        out = self.fc(features)
        return out
