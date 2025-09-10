import logging
import json
import os
from typing import Optional

import azure.functions as func
import joblib
import numpy as np

bp = func.Blueprint()

# Global variable to cache the model
_model: Optional[object] = None

def load_model():
    """Load the model once and cache it"""
    global _model
    if _model is None:
        try:
            # file is named 'penguins_model.pkl' in repo
            model_path = os.path.join(os.path.dirname(__file__), 'penguins_model.pkl')
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model not found at: {model_path}")

            _model = joblib.load(model_path)
            logging.info("Model loaded successfully from %s", model_path)
        except Exception as e:
            logging.exception("Error loading model: %s", e)
            raise
    return _model

@bp.route(route="ClassifyPenguinSimple", methods=["GET", "POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def classify(req: func.HttpRequest) -> func.HttpResponse:
    """Simple penguin classification using pre-loaded model"""
    logging.info("ClassifyPenguinSimple function processed a request.")
    
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
        logging.exception("Error in function: %s", e)
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
