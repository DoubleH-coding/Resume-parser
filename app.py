from flask import Flask, render_template, request
import os
from resume_parser import parse_resume

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['resume']
    if file.filename == '':
        return "No selected file", 400
        
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    extracted_data = parse_resume(filepath)
    return render_template('result.html', data=extracted_data)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
