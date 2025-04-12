#!/usr/bin/env python3
# web_app.py - Flask web application for penguin classifier

from flask import Flask, render_template, request, jsonify
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, 
            static_folder='../static',
            template_folder='../templates')

# Azure Function URL
AZURE_FUNCTION_URL = os.environ.get('AZURE_FUNCTION_URL', 'https://your-azure-function-url.azurewebsites.net/api/ClassifyPenguin')

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    """
    Process the penguin measurements and return predicted species
    Expected JSON format:
    {
        "features": [CulmenLength, CulmenDepth, FlipperLength, BodyMass]
    }
    """
    try:
        # Get request data
        data = request.get_json(force=True)
        features = data.get('features', [])
        
        # Validate input
        if len(features) != 4:
            return jsonify({"error": "Expected 4 features: CulmenLength, CulmenDepth, FlipperLength, BodyMass"}), 400
        
        # Two options for processing:
        # 1. Direct connection to container (simpler for testing)
        if os.environ.get('USE_DIRECT_CONNECTION', 'false').lower() == 'true':
            # Direct connection to the container
            container_url = os.environ.get('CONTAINER_URL', 'http://localhost:5000/predict')
            response = requests.post(
                container_url,
                json={"features": features},
                headers={'Content-Type': 'application/json'}
            )
            
            # Check for error
            if response.status_code != 200:
                return jsonify({"error": f"Container service returned status code {response.status_code}"}), 500
                
            # Get prediction from container
            result = response.json()
            
            # Enhance result with human-readable species names
            penguin_species = ['Adelie', 'Chinstrap', 'Gentoo']
            result['species_name'] = penguin_species[result['prediction']]
            
            return jsonify(result)
            
        # 2. Azure Function connection (production)
        else:
            # Prepare payload for Azure Function
            payload = {
                "features": features
            }
            
            # Call Azure Function to trigger container instance
            response = requests.post(
                AZURE_FUNCTION_URL,
                json=payload,
                headers={'Content-Type': 'application/json'}
            )
            
            # Check for error
            if response.status_code != 200:
                return jsonify({"error": f"Azure Function returned status code {response.status_code}"}), 500
                
            # Return the result from Azure Function
            return jsonify(response.json())
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Debug flag should be set to False in production
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 8080))
    
    # Run the application
    app.run(host='0.0.0.0', port=port, debug=debug_mode)