import logging
import json
import os
from typing import Optional

import azure.functions as func
import joblib
import numpy as np

import shap
import matplotlib

bp = func.Blueprint()

# Global variable to cache the model
_model: Optional[object] = None
_background: Optional[object] = None

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

def load_background():
    global _background
    if _background is None:
        try:
            background_path = os.path.join(os.path.dirname(__file__), '../shared/background_object.pkl')
            if not os.path.exists(background_path):
                raise FileNotFoundError(f"background object not found at {background_path}")
            _background = joblib.load(background_path)
            logging.info("background object loaded successfully")
        except Exception as e:
            logging.exception(f"Error loading background object")
            raise
    return _background

@bp.route(route="XAI", methods=["GET", "POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def xai(req: func.HttpRequest) -> func.HttpResponse:
    """Implementing XAI to class prediction"""
    logging.info("XAI function processed a request from the classify function")
    
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
        new_features = req_body.get('new_features', [])
        predicted_class = req_body.get('predicted_class', -1)
        
        
        # Validate features
        if not new_features or len(new_features) != 4:
            return func.HttpResponse(
                json.dumps({"error": "Features array must contain exactly 4 values"}),
                status_code=400,
                headers=headers,
                mimetype="application/json"
            )
        if not predicted_class or predicted_class == -1:
            return func.HttpResponse(
                json.dumps({'error': 'predicted class returned -1'}),
                status_code=400,
                headers=headers,
                mimetype='application/json'
            )

        new_input = np.array([new_features])
        penguin_features = ["culmen-length", "culmen-depth", "flipper-length", "body-mass"]
 
        # Load model
        model = load_model()

        # load background object
        background = load_background()

        # create explainer object
        explainer = shap.TreeExplainer(
            model,
            data=background,
            model_output='probability',
            feature_perturbation='interventional',
            feature_names=penguin_features
        )
        shap_values = explainer(new_input)
        

        # creating force_plot - decide later how this can be saved, then sent to frontend

        # shap.initjs()
        # shap.plots.force(
        #     explainer.expected_value[predicted_class],
        #     shap_values.values[0, :, predicted_class],
        #     new_input[0],
        #     feature_names = penguin_features
        # )

        values = shap_values.values[0, :, predicted_class]

        # pair with penguin feature names
        feature_importance = list(zip(penguin_features, values))

        # sort by absolute value impact
        sorted_features = sorted(feature_importance, key=lambda x: abs(x[1], reverse=True))

        # top 2
        feat_imp_dict = {}
        top_2 = sorted_features[:2]
        for name,value in top_2:
            feat_imp_dict[name] = round(value, 4)

        classify_payload = {
            "feature_importance": feat_imp_dict
        }


        return func.HttpResponse(
            json.dumps(classify_payload),
            status_code=200,
            headers=headers,
            mimetype="application/json"
        )
    except Exception as e:
        logging.exception(f"Error in xai function: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "error": str(e),
                "success": False,
                "message": "XAI failed"
            }),
            status_code=500,
            headers=headers,
            mimetype="application/json"
        )
