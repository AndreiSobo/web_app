import os
import joblib
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
    penguin_classes = ['first_category', 'sec_category', 'third_category']
    
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

if __name__ == '__main__':
    # Check if model loads correctly
    model = get_model()
    if model is None:
        print(f"Failed to load model from {MODEL_PATH}")
    else:
        print("Model loaded successfully!")
        print(f"Model type: {type(model)}")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)