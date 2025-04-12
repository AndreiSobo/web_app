import logging
import azure.functions as func
import json
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Simple debug endpoint with minimal dependencies"""
    logging.info('Debug endpoint processed a request.')

    # Add CORS headers
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Requested-With"
    }

    # Handle OPTIONS request for CORS preflight
    if req.method == "OPTIONS":
        return func.HttpResponse(status_code=204, headers=headers)
        
    # Return simple JSON response
    return func.HttpResponse(
        json.dumps({
            "status": "success", 
            "message": "Debug endpoint is working!",
            "available_env_vars": [k for k in os.environ.keys()],
            "function_app": "found"
        }),
        mimetype="application/json",
        headers=headers
    )