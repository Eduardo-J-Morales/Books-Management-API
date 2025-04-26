from flask import Flask, request, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'Eduardo_Morales'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 50 

ALLOWED_EXTENSIONS = { 'mp4', 'avi', 'mov' }

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
    
    if file and allowed_file(file.filename)

    return "hola"
if __name__ == '__main__':
    app.run()