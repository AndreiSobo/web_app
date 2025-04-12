import logging
import azure.functions as func
import json
import os
import traceback
import requests
import platform
import sys
from azure.identity import DefaultAzureCredential
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import (
    ContainerGroup, Container, ResourceRequirements, ResourceRequests,
    ImageRegistryCredential, EnvironmentVariable, ContainerGroupNetworkProtocol,
    Port, IpAddress, ContainerGroupIpAddressType
)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
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

    # Log detailed information about the environment and request
    logging.info(f"Python version: {platform.python_version()}")
    logging.info(f"System info: {platform.system()} {platform.release()}")
    logging.info(f"Request URL: {req.url}")
    logging.info(f"Request method: {req.method}")
    logging.info(f"Request headers: {dict(req.headers)}")
    
    # Log available environment variables (excluding sensitive ones)
    env_vars_safe = {k: v for k, v in os.environ.items() 
                     if not any(secret in k.lower() for secret in ["key", "password", "token", "secret"])}
    logging.info(f"Environment variables: {env_vars_safe}")
    
    # Log import paths for troubleshooting
    logging.info(f"Python path: {sys.path}")
    
    try:
        # Get request body
        try:
            req_body = req.get_json()
            logging.info(f"Request body: {req_body}")
        except ValueError:
            logging.warning("Request body is not valid JSON or is empty")
            return func.HttpResponse(
                json.dumps({"error": "Request body must be valid JSON with 'features' array"}),
                status_code=400,
                headers=headers,
                mimetype="application/json"
            )
        
        # Extract penguin features
        features = req_body.get('features', [])
        
        if not features or len(features) != 4:
            logging.warning(f"Invalid features array: {features}")
            return func.HttpResponse(
                json.dumps({
                    "error": "Invalid or missing features array",
                    "details": "Expected an array with exactly 4 numeric values: [culmenLength, culmenDepth, flipperLength, bodyMass]",
                    "received": features
                }),
                status_code=400,
                headers=headers,
                mimetype="application/json"
            )
        
        # Check if we should use bypass mode for testing
        if os.environ.get("BYPASS_CONTAINER", "false").lower() == "true":
            logging.info("BYPASS_CONTAINER is true, returning mock response")
            mock_response = {
                "prediction": 1,
                "class": "Chinstrap",
                "species_name": "Chinstrap",
                "confidence": 0.92,
                "features": features,
                "note": "This is a mock response (BYPASS_CONTAINER=true)"
            }
            return func.HttpResponse(
                json.dumps(mock_response),
                status_code=200,
                headers=headers,
                mimetype="application/json"
            )
            
        # Debug environment variables needed for container instance
        missing_vars = []
        for var in ["AZURE_SUBSCRIPTION_ID", "AZURE_RESOURCE_GROUP", 
                   "CONTAINER_IMAGE", "REGISTRY_SERVER", 
                   "REGISTRY_USERNAME", "REGISTRY_PASSWORD"]:
            if not os.environ.get(var):
                missing_vars.append(var)
        
        if missing_vars:
            logging.error(f"Missing required environment variables: {missing_vars}")
            return func.HttpResponse(
                json.dumps({
                    "error": "Configuration error",
                    "details": f"Missing required environment variables: {missing_vars}",
                    "help": "Please set these variables in the Azure Function App configuration"
                }),
                status_code=500,
                headers=headers,
                mimetype="application/json"
            )
            
        # Start container instance and process the classification
        result = process_with_container(features)
        
        # Return the result
        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            headers=headers,
            mimetype="application/json"
        )
        
    except Exception as e:
        error_details = traceback.format_exc()
        error_type = type(e).__name__
        logging.error(f"Error: {str(e)}\nType: {error_type}\nDetails: {error_details}")
        
        return func.HttpResponse(
            json.dumps({
                "error": str(e),
                "error_type": error_type,
                "details": error_details if os.environ.get("INCLUDE_ERROR_DETAILS", "true").lower() == "true" else "Set INCLUDE_ERROR_DETAILS=true for more info",
                "debug_endpoint": "/api/debug"
            }),
            status_code=500,
            headers=headers,
            mimetype="application/json"
        )

def process_with_container(features):
    """Process the classification request using a container instance"""
    logging.info(f"Starting container processing with features: {features}")
    
    try:
        # Configuration for Azure Container Instance
        subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
        resource_group = os.environ.get("AZURE_RESOURCE_GROUP")
        container_group_name = f"penguin-classifier-{os.urandom(4).hex()}"  # Generate unique name
        container_image = os.environ.get("CONTAINER_IMAGE")
        registry_server = os.environ.get("REGISTRY_SERVER")
        registry_username = os.environ.get("REGISTRY_USERNAME")
        registry_password = os.environ.get("REGISTRY_PASSWORD")
        
        # Log info (without sensitive data)
        logging.info(f"Setting up container: {container_group_name}")
        logging.info(f"Using image: {container_image}")
        logging.info(f"Registry server: {registry_server}")
        
        # Prepare environment variables for the container
        env_vars = [
            EnvironmentVariable(name="MODEL_PATH", value="/app/models/penguins_model.pkl"),
            EnvironmentVariable(name="FEATURES", value=json.dumps(features))
        ]
        
        # Initialize the Container Instance client
        logging.info("Initializing DefaultAzureCredential")
        try:
            credential = DefaultAzureCredential()
            logging.info("DefaultAzureCredential initialized successfully")
        except Exception as auth_error:
            logging.error(f"Error initializing DefaultAzureCredential: {str(auth_error)}")
            raise Exception(f"Authentication failed: {str(auth_error)}")
        
        logging.info("Creating ContainerInstanceManagementClient")
        client = ContainerInstanceManagementClient(credential, subscription_id)
        
        # Define container group
        container_resource_requests = ResourceRequests(memory_in_gb=1.0, cpu=1.0)
        container_resources = ResourceRequirements(requests=container_resource_requests)
        
        container = Container(
            name="penguin-classifier-container",
            image=container_image,
            resources=container_resources,
            environment_variables=env_vars,
            command=["python", "/app/src/app.py", "--classify-only"],
            ports=[Port(port=5000)]
        )
        
        # Registry credentials
        registry_credential = ImageRegistryCredential(
            server=registry_server,
            username=registry_username,
            password=registry_password
        )
        
        # IP address configuration
        group_ip_address = IpAddress(
            ports=[Port(port=5000, protocol=ContainerGroupNetworkProtocol.tcp)],
            type=ContainerGroupIpAddressType.public
        )
        
        # Create container group
        container_group = ContainerGroup(
            location=os.environ.get("AZURE_LOCATION", "eastus"),
            containers=[container],
            os_type="Linux",
            restart_policy="Never",
            image_registry_credentials=[registry_credential],
            ip_address=group_ip_address
        )
        
        # Create the container group
        logging.info(f"Creating container group {container_group_name} in resource group {resource_group}")
        try:
            container_group_creation = client.container_groups.begin_create_or_update(
                resource_group,
                container_group_name,
                container_group
            )
            
            # Wait for the container to complete
            container_group_result = container_group_creation.result()
            logging.info(f"Container group created: {container_group_result.name}")
            logging.info(f"Container group provisioning state: {container_group_result.provisioning_state}")
            
        except Exception as create_error:
            logging.error(f"Error creating container group: {str(create_error)}")
            error_details = traceback.format_exc()
            raise Exception(f"Container creation failed: {str(create_error)}\n{error_details}")
        
        # Get container logs for output
        try:
            logging.info("Retrieving container logs")
            logs = client.containers.list_logs(
                resource_group, 
                container_group_name, 
                "penguin-classifier-container"
            ).content
            
            logging.info(f"Container logs: {logs}")
        except Exception as log_error:
            logging.error(f"Error getting container logs: {str(log_error)}")
            logs = f"Error retrieving logs: {str(log_error)}"
        
        # Parse the logs to get the prediction result
        try:
            # Try to extract JSON output from container logs
            import re
            json_match = re.search(r'({.*})', logs)
            if json_match:
                result_json = json_match.group(1)
                result = json.loads(result_json)
                logging.info(f"Successfully parsed result: {result}")
            else:
                # If no JSON found, return a formatted message
                logging.warning("No JSON found in container logs")
                result = {
                    "error": "Container did not return valid JSON output",
                    "logs": logs
                }
        except Exception as parse_error:
            logging.error(f"Error parsing container output: {str(parse_error)}")
            result = {
                "error": f"Failed to parse container output: {str(parse_error)}",
                "logs": logs
            }
        
        # Enhance result with human-readable species names if prediction exists
        if "prediction" in result and result["prediction"] in (0, 1, 2):
            penguin_species = ['Adelie', 'Chinstrap', 'Gentoo']
            result['species_name'] = penguin_species[result['prediction']]
        
        # Clean up - delete the container group
        logging.info(f"Deleting container group {container_group_name}")
        try:
            client.container_groups.begin_delete(resource_group, container_group_name)
            logging.info("Container group deletion initiated")
        except Exception as delete_error:
            logging.error(f"Error deleting container group: {str(delete_error)}")
        
        return result
        
    except Exception as e:
        error_details = traceback.format_exc()
        logging.error(f"Error in container processing: {str(e)}\n{error_details}")
        return {
            "error": str(e),
            "error_type": type(e).__name__,
            "details": error_details
        }