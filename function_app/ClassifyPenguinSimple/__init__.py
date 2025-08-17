import logging
import azure.functions as func
import json
import joblib
import os
import numpy as np

# Global variable to cache the model
_model = None

def load_model():
    """Load the model once and cache it"""
    global _model
    if _model is None:
        try:
            # Try multiple possible paths for the model
            possible_paths = [
                os.path.join(os.path.dirname(__file__), 'penguins_model.pkl'),  # Same directory as function
                os.path.join(os.path.dirname(__file__), '..', 'models', 'penguins_model.pkl'),  # models folder
                os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'penguins_model.pkl'),  # Original path
            ]
            
            model_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    model_path = path
                    break
            
            if model_path is None:
                raise FileNotFoundError(f"Model not found in any of these paths: {possible_paths}")
            
            _model = joblib.load(model_path)
            logging.info(f"Model loaded successfully from {model_path}")
        except Exception as e:
            logging.error(f"Error loading model: {str(e)}")
            raise e
    return _model

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Simple penguin classification using pre-loaded model"""
    logging.info('ClassifyPenguinSimple function processed a request.')
    
    # CORS headers
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Requested-With"
    }
    
    # Handle OPTIONS request for CORS preflight
    if req.method == "OPTIONS":
        return func.HttpResponse(status_code=204, headers=headers)
    
    try:
        # Get request body
        req_body = req.get_json()
        if not req_body:
            return func.HttpResponse(
                json.dumps({"error": "Request body is required"}),
                status_code=400,
                headers=headers,
                mimetype="application/json"
            )
        
        features = req_body.get('features', [])
        
        # Validate features
        if not features or len(features) != 4:
            return func.HttpResponse(
                json.dumps({"error": "Features array must contain exactly 4 values"}),
                status_code=400,
                headers=headers,
                mimetype="application/json"
            )
        
        # Load model
        model = load_model()
        
        # Make prediction
        features_array = np.array([features])
        prediction = int(model.predict(features_array)[0])
        
        # Get probabilities if available
        try:
            probabilities = model.predict_proba(features_array)[0]
            confidence = float(max(probabilities))
        except AttributeError:
            confidence = None
        
        # Species mapping
        penguin_species = ['Adelie', 'Chinstrap', 'Gentoo']
        species_name = penguin_species[prediction]
        
        # Response
        response = {
            "prediction": prediction,
            "class": species_name,
            "species_name": species_name,
            "features": features,
            "success": True
        }
        
        if confidence is not None:
            response["confidence"] = confidence
        
        return func.HttpResponse(
            json.dumps(response),
            status_code=200,
            headers=headers,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Error in function: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "error": str(e),
                "success": False,
                "message": "Classification failed"
            }),
            status_code=500,
            headers=headers,
            mimetype="application/json"
        )
