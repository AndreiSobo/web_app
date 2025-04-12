import logging
import azure.functions as func
import json
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Simplified function to test basic functionality without container dependencies"""
    logging.info('ClassifyPenguin function processed a request.')
    
    # Add CORS headers for all responses
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Requested-With"
    }
    
    # Handle OPTIONS request for CORS preflight
    if req.method == "OPTIONS":
        logging.info("Handling OPTIONS preflight request")
        return func.HttpResponse(
            status_code=204,
            headers=headers
        )
    
    try:
        # Get request body
        try:
            req_body = req.get_json()
            logging.info(f"Request body: {req_body}")
            features = req_body.get('features', [])
        except ValueError:
            features = []
            logging.warning("Request body is not valid JSON or is empty")
        
        # Return mock response without container processing
        mock_response = {
            "success": True,
            "prediction": 1,
            "class": "Chinstrap",
            "species_name": "Chinstrap",
            "confidence": 0.92,
            "features": features,
            "note": "This is a mock response (no container processing)",
            "env_vars_available": [k for k in os.environ.keys() if not any(secret in k.lower() for secret in ["key", "password", "token", "secret"])]
        }
        
        return func.HttpResponse(
            json.dumps(mock_response),
            status_code=200,
            headers=headers,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Error in simplified function: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "error": str(e),
                "message": "Error in simplified ClassifyPenguin function"
            }),
            status_code=500,
            headers=headers,
            mimetype="application/json"
        )