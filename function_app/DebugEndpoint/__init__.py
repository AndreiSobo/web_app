import logging
import azure.functions as func
import json
import os
import platform

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Simple debug endpoint to test basic functionality without dependencies"""
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
        
    try:
        # Get environment information
        env_info = {
            "python_version": platform.python_version(),
            "system": platform.system(),
            "node": platform.node(),
            "environment_variables": {
                k: v for k, v in os.environ.items() 
                if not any(secret in k.lower() for secret in ["key", "password", "token", "secret"])
            },
            "headers": dict(req.headers),
            "url": req.url,
            "method": req.method,
        }
        
        # Try to get request body if available
        try:
            req_body = req.get_json()
            env_info["request_body"] = req_body
        except ValueError:
            env_info["request_body"] = "No JSON body or parsing failed"
            
        return func.HttpResponse(
            json.dumps({"status": "success", "debug_info": env_info}, indent=2),
            mimetype="application/json",
            headers=headers
        )
    except Exception as e:
        logging.exception("Exception in debug endpoint")
        return func.HttpResponse(
            json.dumps({"status": "error", "error": str(e), "error_type": type(e).__name__}),
            status_code=500,
            mimetype="application/json",
            headers=headers
        )