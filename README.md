# Deepfake Detection Portal 🔍🤖

A web-based platform designed to detect deepfake videos using deep learning. This portal allows users to upload video files, analyzes frames for synthetic manipulations, and highlights the most suspicious segments with confidence scores. Leveraging a ResNet50 backbone with a custom classifier, it aims to provide an intuitive interface for identifying AI-generated content, crucial in combating misinformation.

![Flask](https://img.shields.io/badge/Flask-2.3.2-%23000.svg?logo=flask)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-%23EE4C2C.svg?logo=pytorch)
![OpenCV](https://img.shields.io/badge/OpenCV-4.7-%235C3EE8.svg?logo=opencv)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-%237952B3.svg?logo=bootstrap)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?logo=python)
![License](https://img.shields.io/badge/License-MIT-green.svg)

🌐 #Live Demo

## 🧬 Core Features
- **Video Upload Support**: Accepts MP4, AVI, and MOV files up to 50MB.
- **Frame Sampling**: Analyzes every 30th frame for efficient processing.
- **Deepfake Detection Model**: Uses ResNet50 pre-trained on ImageNet with a custom classifier (512-layer DNN + sigmoid activation).
- **Suspicious Frame Highlighting**: Ranks and displays top 5 frames with highest deepfake probability.
- **Interactive Results**: Shows analyzed video alongside flagged frames with timestamps.
- **Confidence Metric**: Aggregates scores from suspicious frames into a percentage-based risk assessment.

## 🚀 Installation

git clone https://github.com/yourusername/deepfake-detection-portal.git
cd Deepfake-Detection-Portal
