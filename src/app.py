import os
import joblib
import json
import sys
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
MODEL_PATH = os.environ.get('MODEL_PATH', '../models/penguins_model.pkl')

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"})

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint to make predictions
    Expected JSON format:
    {
        "features": [CulmenLength, CulmenDepth, FlipperLength, BodyMass]
    }
    """
    # Get model
    model = get_model()
    
    # Parse request data
    data = request.get_json(force=True)
    features = data.get('features', [])
    
    # Validate input
    if len(features) != 4:
        return jsonify({"error": "Expected 4 features: CulmenLength, CulmenDepth, FlipperLength, BodyMass"}), 400
    
    # Make prediction
    prediction = int(model.predict([features])[0])
    
    # Get class names (these should match what you used in training)
    penguin_classes = ['Adelie', 'Chinstrap', 'Gentoo']
    
    # Return prediction result
    return jsonify({
        "prediction": prediction,
        "class": penguin_classes[prediction]
    })

def get_model():
    """Load the model only once and cache it"""
    if not hasattr(get_model, 'model'):
        try:
            get_model.model = joblib.load(MODEL_PATH)
            print(f"Model loaded from {MODEL_PATH}")
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            return None
    return get_model.model

def classify_from_env():
    """Classify penguin based on features from environment variable"""
    try:
        # Get features from environment variable
        features_str = os.environ.get('FEATURES')
        if not features_str:
            print(json.dumps({"error": "No features provided in FEATURES environment variable"}))
            return 1
            
        # Parse features
        features = json.loads(features_str)
        
        # Validate features
        if len(features) != 4:
            print(json.dumps({"error": "Expected 4 features: CulmenLength, CulmenDepth, FlipperLength, BodyMass"}))
            return 1
            
        # Load model
        model = get_model()
        if model is None:
            print(json.dumps({"error": f"Failed to load model from {MODEL_PATH}"}))
            return 1
            
        # Make prediction
        prediction = int(model.predict([features])[0])
        
        # Get class names
        penguin_classes = ['Adelie', 'Chinstrap', 'Gentoo']
        
        # Output prediction as JSON
        result = {
            "prediction": prediction,
            "class": penguin_classes[prediction],
            "features": features
        }
        
        print(json.dumps(result))
        return 0
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        return 1

if __name__ == '__main__':
    # Check if we're in classify-only mode (for container instances)
    if len(sys.argv) > 1 and sys.argv[1] == '--classify-only':
        sys.exit(classify_from_env())
    
    # Normal mode: Check if model loads correctly
    model = get_model()
    if model is None:
        print(f"Failed to load model from {MODEL_PATH}")
    else:
        print("Model loaded successfully!")
        print(f"Model type: {type(model)}")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)