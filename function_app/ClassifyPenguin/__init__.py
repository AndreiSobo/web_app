import logging
import azure.functions as func
import json
import os
import traceback
import requests
from azure.identity import DefaultAzureCredential
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import (
    ContainerGroup, Container, ResourceRequirements, ResourceRequests,
    ImageRegistryCredential, EnvironmentVariable, ContainerGroupNetworkProtocol,
    Port, IpAddress, ContainerGroupIpAddressType
)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # Add CORS headers
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Requested-With"
    }
    
    # Handle OPTIONS request for CORS preflight
    if req.method == "OPTIONS":
        return func.HttpResponse(
            status_code=204,
            headers=headers
        )
    
    try:
        # Log request details for debugging
        logging.info(f"Request method: {req.method}")
        logging.info(f"Request URL: {req.url}")
        logging.info(f"Request headers: {dict(req.headers)}")
        
        # Get request body
        try:
            req_body = req.get_json()
            logging.info(f"Request body: {req_body}")
        except ValueError:
            logging.warning("Request body is not valid JSON or is empty")
            return func.HttpResponse(
                json.dumps({"error": "Request body must be valid JSON"}),
                status_code=400,
                headers=headers,
                mimetype="application/json"
            )
        
        # Extract penguin features
        features = req_body.get('features', [])
        
        if not features or len(features) != 4:
            logging.warning(f"Invalid features: {features}")
            return func.HttpResponse(
                json.dumps({"error": "Invalid or missing features. Expected 4 features: CulmenLength, CulmenDepth, FlipperLength, BodyMass"}),
                status_code=400,
                headers=headers,
                mimetype="application/json"
            )
        
        # Log environment variables for debugging (masking sensitive values)
        env_vars = {
            "AZURE_SUBSCRIPTION_ID": os.environ.get("AZURE_SUBSCRIPTION_ID", "Not set"),
            "AZURE_RESOURCE_GROUP": os.environ.get("AZURE_RESOURCE_GROUP", "Not set"),
            "CONTAINER_IMAGE": os.environ.get("CONTAINER_IMAGE", "Not set"),
            "REGISTRY_SERVER": os.environ.get("REGISTRY_SERVER", "Not set"),
            "REGISTRY_USERNAME": "******" if os.environ.get("REGISTRY_USERNAME") else "Not set",
            "REGISTRY_PASSWORD": "******" if os.environ.get("REGISTRY_PASSWORD") else "Not set",
        }
        logging.info(f"Environment variables: {env_vars}")
        
        # For quick testing without container, return sample response
        if os.environ.get("BYPASS_CONTAINER", "false").lower() == "true":
            logging.info("Bypassing container and returning sample response")
            sample_response = {
                "prediction": 1,
                "class": "Chinstrap",
                "species_name": "Chinstrap",
                "confidence": 0.92,
                "features": features,
                "note": "This is a sample response, container was bypassed"
            }
            return func.HttpResponse(
                json.dumps(sample_response),
                status_code=200,
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
        logging.error(f"Error processing request: {str(e)}\n{error_details}")
        return func.HttpResponse(
            json.dumps({
                "error": str(e),
                "details": error_details if os.environ.get("INCLUDE_ERROR_DETAILS", "false").lower() == "true" else "Enable INCLUDE_ERROR_DETAILS in function settings for more information"
            }),
            status_code=500,
            headers=headers,
            mimetype="application/json"
        )

def process_with_container(features):
    # Configuration for Azure Container Instance
    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    resource_group = os.environ.get("AZURE_RESOURCE_GROUP")
    container_group_name = f"penguin-classifier-{os.urandom(4).hex()}"  # Generate unique name
    container_image = os.environ.get("CONTAINER_IMAGE")  # e.g., "myregistry.azurecr.io/penguin-classifier:latest"
    registry_server = os.environ.get("REGISTRY_SERVER")
    registry_username = os.environ.get("REGISTRY_USERNAME")
    registry_password = os.environ.get("REGISTRY_PASSWORD")
    
    # Log container setup
    logging.info(f"Setting up container: {container_group_name}")
    logging.info(f"Using image: {container_image}")
    
    # Prepare environment variables for the container
    env_vars = [
        EnvironmentVariable(name="MODEL_PATH", value="/app/models/penguins_model.pkl"),
        EnvironmentVariable(name="FEATURES", value=json.dumps(features))
    ]
    
    try:
        # Initialize the Container Instance client
        logging.info("Initializing DefaultAzureCredential")
        credential = DefaultAzureCredential()
        
        logging.info("Initializing ContainerInstanceManagementClient")
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
        logging.info(f"Creating container group {container_group_name}")
        container_group_creation = client.container_groups.begin_create_or_update(
            resource_group,
            container_group_name,
            container_group
        )
        
        # Wait for the container to complete
        container_group_result = container_group_creation.result()
        logging.info(f"Container group created: {container_group_result.name}")
        
        # Get container logs for output
        logs = client.containers.list_logs(
            resource_group, 
            container_group_name, 
            "penguin-classifier-container"
        ).content
        
        logging.info(f"Container logs: {logs}")
        
        # Parse the logs to get the prediction result
        try:
            # Try to extract JSON output from container logs
            import re
            json_match = re.search(r'({.*})', logs)
            if json_match:
                result_json = json_match.group(1)
                result = json.loads(result_json)
            else:
                # If no JSON found, return a formatted message
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
        client.container_groups.begin_delete(resource_group, container_group_name)
        
        return result
        
    except Exception as e:
        error_details = traceback.format_exc()
        logging.error(f"Error in container processing: {str(e)}\n{error_details}")
        raise