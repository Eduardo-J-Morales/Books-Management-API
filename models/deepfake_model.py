import torch
import cv2
import numpy as np
from torchvision import transforms
from torchvision.models import resnet50,  ResNet50_Weights

weights = ResNet50_Weights.DEFAULT
model = resnet50(weights=weights)
model.eval()
preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((224, 224)),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def predict_deepfake(frames):
    features = []
    for frame in frames:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        input_tensor = preprocess(frame_rgb)
        input_batch = input_tensor.unsqueeze(0)

        with torch.no_grad():
            features.append(model(input_batch).squeeze().numpy())

    confidence = np.mean([f.mean() for f in features])
    return float(np.clip(confidence, 0.3, 0.7))