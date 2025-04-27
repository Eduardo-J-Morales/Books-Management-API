import torch
import cv2
import numpy as np
from torch import nn
from torchvision import transforms
from torchvision.models import resnet50, ResNet50_Weights

class DeepfakeDetector(nn.Module):
    def __init__(self):
        super().__init__()
        self.backbone = resnet50(weights=ResNet50_Weights.DEFAULT)
        self.classifier = nn.Sequential(
            nn.Linear(1000, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, 1),
            nn.Sigmoid()
        )
        
        for param in self.backbone.parameters():
            param.requires_grad = False
            
    def forward(self, x):
        features = self.backbone(x)
        return self.classifier(features)

model = DeepfakeDetector()
model.eval()

preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((224, 224)),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def predict_deepfake(frames):
    frame_scores = []
    for frame in frames:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        input_tensor = preprocess(frame_rgb).unsqueeze(0)
        
        with torch.no_grad():
            score = model(input_tensor).item()
        
        frame_scores.append(score)
    
    return frame_scores