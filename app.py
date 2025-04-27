import os
import cv2
import numpy as np
from flask import Flask, request, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from models.deepfake_model import predict_deepfake

app = Flask(__name__)
app.secret_key = 'Eduardo_Morales'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 50 

ALLOWED_EXTENSIONS = { 'mp4', 'avi', 'mov' }

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_video():
    if 'file' not in request.files:
        flash('No selected file')
        return redirect(url_for('home'))

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('home'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        confidence, suspicious_frames = process_video(filepath)

        return render_template('result.html',
                               filename=filename,
                               confidence=confidence,
                               frames=suspicious_frames
                               )
    
def process_video(filepath):
    cap = cv2.VideoCapture(filepath)
    frames = []
    frame_numbers = []
    count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        if count % 30 == 0:
            frames.append(frame)
            frame_numbers.append(count)
        count += 1
    cap.release()

    frame_scores = predict_deepfake(frames)
    
    scored_frames = list(zip(frame_numbers, frames, frame_scores))
    scored_frames.sort(key=lambda x: x[2], reverse=True)  
    top_suspicious = scored_frames[:5]

    suspicious_frames = []
    output_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'frames')
    os.makedirs(output_dir, exist_ok=True)
    
    for idx, frame, score in top_suspicious:
        frame_path = os.path.join('frames', f'frame_{idx}.jpg')
        full_path = os.path.join(app.config['UPLOAD_FOLDER'], frame_path)
        cv2.imwrite(full_path, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        suspicious_frames.append((idx, frame_path))
    
    confidence = np.mean([score for _, _, score in top_suspicious])
    
    return confidence, suspicious_frames


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0')
