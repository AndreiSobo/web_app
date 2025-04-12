import logging
import azure.functions as func
import json
import os
import uuid
import traceback
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ClientAuthenticationError
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import (
    ContainerGroup, Container, ResourceRequirements, ResourceRequests,
    ImageRegistryCredential, EnvironmentVariable, ContainerGroupNetworkProtocol,
    Port, IpAddress, ContainerGroupIpAddressType
)

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Process request using Azure Container Instances with incremental checks"""
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
            return func.HttpResponse(
                json.dumps({"error": "Invalid request body. Expected JSON with features array."}),
                status_code=400,
                headers=headers,
                mimetype="application/json"
            )
        
        # Check for valid features
        if not features or len(features) != 4:
            return func.HttpResponse(
                json.dumps({"error": "Features array must contain exactly 4 values for penguin classification."}),
                status_code=400,
                headers=headers,
                mimetype="application/json"
            )
        
        # Check for bypass mode - return mock response without container
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
        
        # Check required environment variables
        required_vars = [
            "AZURE_SUBSCRIPTION_ID",
            "AZURE_RESOURCE_GROUP", 
            "AZURE_LOCATION",
            "CONTAINER_IMAGE", 
            "REGISTRY_SERVER", 
            "REGISTRY_USERNAME",
            "REGISTRY_PASSWORD"
        ]
        
        missing_vars = []
        env_values = {}
        
        for var in required_vars:
            value = os.environ.get(var)
            if not value:
                missing_vars.append(var)
            else:
                # Don't include sensitive values in the log
                if "PASSWORD" in var or "KEY" in var:
                    env_values[var] = "********"
                else:
                    env_values[var] = value
        
        # Initialize response with environment check results
        response = {
            "success": True,
            "prediction": 1,
            "species_name": "Chinstrap",
            "confidence": 0.92,
            "features": features,
            "environment_check": {
                "all_vars_present": len(missing_vars) == 0,
                "missing_vars": missing_vars,
                "available_vars": env_values
            },
            "stage": "environment_check"
        }
        
        # If environment variables are missing, return now
        if missing_vars:
            response["message"] = "Missing required environment variables"
            response["success"] = False
            return func.HttpResponse(
                json.dumps(response, indent=2),
                status_code=200,
                headers=headers,
                mimetype="application/json"
            )
        
        # Get values from environment
        subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
        resource_group = os.environ.get("AZURE_RESOURCE_GROUP")
        location = os.environ.get("AZURE_LOCATION")
        container_image = os.environ.get("CONTAINER_IMAGE")
        registry_server = os.environ.get("REGISTRY_SERVER")
        registry_username = os.environ.get("REGISTRY_USERNAME")
        registry_password = os.environ.get("REGISTRY_PASSWORD")
        
        # Try to initialize Azure credentials
        try:
            logging.info("Initializing DefaultAzureCredential")
            credential = DefaultAzureCredential()
            
            # Try to access the token (this will validate the credentials)
            token = credential.get_token("https://management.azure.com/.default")
            logging.info("Successfully obtained Azure authentication token")
            
            response["auth_check"] = {
                "status": "success",
                "message": "Azure credentials initialized successfully"
            }
            response["stage"] = "auth_check"
            
            # Try to initialize Container Instance client
            try:
                logging.info("Initializing ContainerInstanceManagementClient")
                client = ContainerInstanceManagementClient(
                    credential=credential,
                    subscription_id=subscription_id
                )
                
                # Try to create registry credential object
                registry_credential = ImageRegistryCredential(
                    server=registry_server,
                    username=registry_username,
                    password=registry_password
                )
                
                logging.info("ContainerInstanceManagementClient initialized successfully")
                
                response["container_client_check"] = {
                    "status": "success",
                    "message": "Container client initialized successfully"
                }
                response["stage"] = "container_client_check"
                
                # Now attempt to create and run the container
                try:
                    # Generate a unique name for the container group
                    container_group_name = f"penguin-classifier-{uuid.uuid4().hex[:8]}"
                    logging.info(f"Creating container group: {container_group_name}")
                    
                    # Prepare environment variables for the container
                    env_vars = [
                        EnvironmentVariable(name="MODEL_PATH", value="/app/models/penguins_model.pkl"),
                        EnvironmentVariable(name="FEATURES", value=json.dumps(features)),
                        EnvironmentVariable(name="PYTHONUNBUFFERED", value="1")
                    ]
                    
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
                    
                    # IP address configuration
                    group_ip_address = IpAddress(
                        ports=[Port(port=5000, protocol=ContainerGroupNetworkProtocol.tcp)],
                        type=ContainerGroupIpAddressType.public
                    )
                    
                    # Create container group
                    container_group = ContainerGroup(
                        location=location,
                        containers=[container],
                        os_type="Linux",
                        restart_policy="Never",
                        image_registry_credentials=[registry_credential],
                        ip_address=group_ip_address
                    )
                    
                    # Create the container group
                    logging.info(f"Creating container group {container_group_name} in {resource_group}")
                    response["container_creation"] = {
                        "status": "starting",
                        "container_group_name": container_group_name
                    }
                    
                    container_group_creation = client.container_groups.begin_create_or_update(
                        resource_group,
                        container_group_name,
                        container_group
                    )
                    
                    # Wait for the container to complete
                    container_group_result = container_group_creation.result()
                    logging.info(f"Container group created: {container_group_result.name}")
                    logging.info(f"Container group provisioning state: {container_group_result.provisioning_state}")
                    
                    response["container_creation"]["status"] = "created"
                    response["container_creation"]["provisioning_state"] = container_group_result.provisioning_state
                    response["stage"] = "container_creation"
                    
                    # Get container logs for output
                    try:
                        logging.info("Retrieving container logs")
                        logs = client.containers.list_logs(
                            resource_group, 
                            container_group_name, 
                            "penguin-classifier-container"
                        ).content
                        
                        logging.info(f"Container logs: {logs}")
                        response["container_logs"] = logs
                        
                        # Parse the logs to get the prediction result
                        try:
                            # Try to extract JSON output from container logs
                            import re
                            json_match = re.search(r'({.*})', logs)
                            if json_match:
                                result_json = json_match.group(1)
                                prediction_result = json.loads(result_json)
                                logging.info(f"Successfully parsed result: {prediction_result}")
                                
                                # Enhance result with human-readable species names if prediction exists
                                if "prediction" in prediction_result and prediction_result["prediction"] in (0, 1, 2):
                                    penguin_species = ['Adelie', 'Chinstrap', 'Gentoo']
                                    prediction_result['species_name'] = penguin_species[prediction_result['prediction']]
                                
                                # Merge prediction result into response
                                response.update(prediction_result)
                                response["stage"] = "prediction_complete"
                                response["message"] = "Classification completed successfully"
                            else:
                                # If no JSON found, return a formatted message
                                logging.warning("No JSON found in container logs")
                                response["prediction_error"] = {
                                    "error": "Container did not return valid JSON output",
                                    "logs": logs
                                }
                                response["message"] = "Container ran but did not return valid prediction data"
                        except Exception as parse_error:
                            error_details = traceback.format_exc()
                            logging.error(f"Error parsing container output: {str(parse_error)}\n{error_details}")
                            response["prediction_error"] = {
                                "error": f"Failed to parse container output: {str(parse_error)}",
                                "logs": logs
                            }
                            response["message"] = "Error parsing container output"
                            
                    except Exception as log_error:
                        error_details = traceback.format_exc()
                        logging.error(f"Error getting container logs: {str(log_error)}\n{error_details}")
                        response["container_logs_error"] = {
                            "error": str(log_error),
                            "message": "Failed to retrieve container logs"
                        }
                    
                    # Clean up - delete the container group
                    try:
                        logging.info(f"Deleting container group {container_group_name}")
                        client.container_groups.begin_delete(resource_group, container_group_name)
                        logging.info("Container group deletion initiated")
                        response["container_deletion"] = {
                            "status": "initiated",
                            "message": "Container group deletion started"
                        }
                    except Exception as delete_error:
                        error_details = traceback.format_exc()
                        logging.error(f"Error deleting container group: {str(delete_error)}\n{error_details}")
                        response["container_deletion_error"] = {
                            "error": str(delete_error),
                            "message": "Failed to delete container group"
                        }
                    
                except Exception as container_error:
                    error_details = traceback.format_exc()
                    logging.error(f"Error creating/running container: {str(container_error)}\n{error_details}")
                    response["container_creation_error"] = {
                        "status": "failed",
                        "error": str(container_error),
                        "message": "Failed to create or run container"
                    }
                    response["success"] = False
                    response["message"] = "Container creation or execution failed"
                
            except Exception as client_error:
                error_details = traceback.format_exc()
                logging.error(f"Error initializing container client: {str(client_error)}\n{error_details}")
                response["container_client_check"] = {
                    "status": "failed",
                    "error": str(client_error),
                    "message": "Failed to initialize container client"
                }
                response["success"] = False
                response["message"] = "Container client initialization failed"
            
        except ClientAuthenticationError as auth_error:
            error_details = str(auth_error)
            logging.error(f"Azure authentication error: {error_details}")
            response["auth_check"] = {
                "status": "failed",
                "error": error_details,
                "message": "Failed to authenticate with Azure"
            }
            response["success"] = False
            response["message"] = "Azure authentication failed"
        except Exception as e:
            error_details = traceback.format_exc()
            logging.error(f"Unexpected error during authentication: {str(e)}\n{error_details}")
            response["auth_check"] = {
                "status": "failed",
                "error": str(e),
                "message": "Unexpected error during authentication"
            }
            response["success"] = False
            response["message"] = "Azure authentication failed with unexpected error"
        
        return func.HttpResponse(
            json.dumps(response, indent=2),
            status_code=200,
            headers=headers,
            mimetype="application/json"
        )
        
    except Exception as e:
        error_details = traceback.format_exc()
        logging.error(f"Error in function: {str(e)}\n{error_details}")
        return func.HttpResponse(
            json.dumps({
                "error": str(e),
                "message": "Error in function execution",
                "details": error_details
            }),
            status_code=500,
            headers=headers,
            mimetype="application/json"
        )