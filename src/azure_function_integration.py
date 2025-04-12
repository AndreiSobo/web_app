# azure_function_integration.py
# This file contains the code for an Azure Function that will be triggered by the Flask app
# and will in turn trigger the Azure Container Instance with your neural network model

import logging
import azure.functions as func
import json
import base64
import os
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

    try:
        # Get request body
        req_body = req.get_json()
        
        # Extract image and parameters
        image_base64 = req_body.get('image')
        parameters = req_body.get('parameters', 0)
        
        if not image_base64:
            return func.HttpResponse(
                json.dumps({"error": "No image provided in request body"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Start container instance and process image
        result = process_with_container(image_base64, parameters)
        
        # Return the result
        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

def process_with_container(image_base64, parameters):
    # Configuration for Azure Container Instance
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    resource_group = os.environ["AZURE_RESOURCE_GROUP"]
    container_group_name = f"neural-network-{os.urandom(4).hex()}"  # Generate unique name
    container_image = os.environ["CONTAINER_IMAGE"]  # e.g., "myregistry.azurecr.io/my-neural-network:latest"
    registry_server = os.environ["REGISTRY_SERVER"]
    registry_username = os.environ["REGISTRY_USERNAME"]
    registry_password = os.environ["REGISTRY_PASSWORD"]
    
    # Prepare environment variables for the container
    env_vars = [
        EnvironmentVariable(name="IMAGE_BASE64", value=image_base64),
        EnvironmentVariable(name="PARAMETERS", value=str(parameters))
    ]
    
    try:
        # Initialize the Container Instance client
        credential = DefaultAzureCredential()
        client = ContainerInstanceManagementClient(credential, subscription_id)
        
        # Define container group
        container_resource_requests = ResourceRequests(memory_in_gb=4.0, cpu=2.0)
        container_resources = ResourceRequirements(requests=container_resource_requests)
        
        container = Container(
            name="neural-network-container",
            image=container_image,
            resources=container_resources,
            environment_variables=env_vars,
            ports=[Port(port=80)]
        )
        
        # Registry credentials
        registry_credential = ImageRegistryCredential(
            server=registry_server,
            username=registry_username,
            password=registry_password
        )
        
        # IP address configuration
        group_ip_address = IpAddress(
            ports=[Port(port=80, protocol=ContainerGroupNetworkProtocol.tcp)],
            type=ContainerGroupIpAddressType.public
        )
        
        # Create container group
        container_group = ContainerGroup(
            location=os.environ["AZURE_LOCATION"],
            containers=[container],
            os_type="Linux",
            restart_policy="Never",
            image_registry_credentials=[registry_credential],
            ip_address=group_ip_address
        )
        
        # Create the container group
        container_group_creation = client.container_groups.begin_create_or_update(
            resource_group,
            container_group_name,
            container_group
        )
        
        # Wait for the container to complete
        container_group_result = container_group_creation.result()
        
        # Get container logs (contains the processing results)
        logs = client.containers.list_logs(
            resource_group, 
            container_group_name, 
            "neural-network-container"
        ).content
        
        # Parse the logs to get the result (assuming the container outputs JSON)
        result = json.loads(logs)
        
        # Clean up - delete the container group
        client.container_groups.begin_delete(resource_group, container_group_name)
        
        return result
        
    except Exception as e:
        logging.error(f"Error in container processing: {str(e)}")
        raise