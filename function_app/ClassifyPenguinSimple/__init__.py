import logging
import json
import os
from typing import Optional

import azure.functions as func
import joblib
import numpy as np
import requests

bp = func.Blueprint()

# Global variable to cache the model
_model: Optional[object] = None

def load_model():
    """Load the model once and cache it"""
    global _model
    if _model is None:
        try:
            # file is named 'penguins_model.pkl' in repo
            model_path = os.path.join(os.path.dirname(__file__), '../shared/penguins_model.pkl')
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model not found at: {model_path}")

            _model = joblib.load(model_path)
            logging.info(f"Model loaded successfully from {model_path}")
        except Exception as e:
            logging.exception("Error loading model: %s", e)
            raise
    return _model

# TODO improve this function to use secrets for function app url
def get_xai_endpoint():
    function_app_url = os.getenv('WEBSITE_HOSTNAME', 'penguin-classifier-consumption-dngqgqbga0g2eqgy.northeurope-01.azurewebsites.net')
    return f'https://{function_app_url}/api/XAI'

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

        # xai payload
        top_features = []

        xai_payload = {
            "new_features": features,
            'predicted_class': prediction
        }
        
        try:
            xai_url = get_xai_endpoint()
            
            # make http request to xai function
            xai_response = requests.post(
                xai_url,
                json=xai_payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )

            if xai_response.status_code == 200:
                xai_data = xai_response.json()
                feature_importance = xai_data.get('feature_importance', {})

                # add the force plot string
                force_plot_string = xai_data.get('force_plot_string', None)

                top_features = [
                    {'name': name, 'impact': impact}
                    for name, impact in feature_importance.items()
                ]
                logging.info(f"successfully got xai data: {top_features}")
            else:
                logging.warning(f"XAI function returned status: {xai_response.status_code}")
        except Exception as e:
            logging.warning(f"an error occured while implementing XAI.: {str(e)}")

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

        if top_features is not None:
            response['top_features'] = top_features
            
        if force_plot_string is not None:
            response['force_plot_string'] = force_plot_string

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
