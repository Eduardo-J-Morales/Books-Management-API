import os
import cv2
import numpy as np
from flask import Flask, request, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

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

def process_video(filepath): 

    cap = cv2.VideoCapture(filepath)
    frames = []
    while cap.isOpend():
        ret, frame = cap.read()
        if not ret: break
        frames.append(frame)
    cap.release()

    suspicious_frames= [
        (i, os.path.join('uploads', f'frame_${i}.jpg'))
        for i in range(0, len(frames), len(frames) // 5)
    ]
    return suspicious_frames[:5]

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run()