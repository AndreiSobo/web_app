# app.py
from flask import Flask, render_template, request, jsonify, url_for
import base64
import os
import requests
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.config['AZURE_FUNCTION_URL'] = 'https://your-azure-function-url.azurewebsites.net/api/ProcessImage'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    # Check if the post request has the file part
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected for uploading'}), 400
    
    # Get numerical parameter
    parameter = request.form.get('parameter', '0')
    try:
        parameter = float(parameter)
    except ValueError:
        return jsonify({'error': 'Parameter must be a number'}), 400
    
    # Save the file temporarily
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Convert image to base64
    with open(filepath, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Prepare payload for Azure Function
    payload = {
        'image': encoded_image,
        'parameters': parameter
    }
    
    try:
        # Call Azure Function
        response = requests.post(
            app.config['AZURE_FUNCTION_URL'],
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code != 200:
            return jsonify({'error': f'Azure Function returned status code {response.status_code}'}), 500
        
        result = response.json()
        
        # Save the processed image
        processed_filename = 'processed_' + filename
        processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
        
        with open(processed_filepath, 'wb') as f:
            f.write(base64.b64decode(result['processedImage']))
        
        return jsonify({
            'original_image': url_for('static', filename=f'uploads/{filename}'),
            'processed_image': url_for('static', filename=f'uploads/{processed_filename}'),
            'output_metrics': result.get('outputMetrics', 'Processing complete')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)