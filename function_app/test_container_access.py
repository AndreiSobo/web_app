"""
Test script to verify Azure Container Registry access
Run with: python test_container_access.py
"""

import os
import json
import sys
from pathlib import Path
from azure.identity import DefaultAzureCredential, AzureCliCredential
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import (
    ImageRegistryCredential
)

def load_dotenv(dotenv_path):
    """Load environment variables from .env file"""
    try:
        with open(dotenv_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                key, value = line.split('=', 1)
                os.environ[key] = value
        print(f"✅ Loaded environment variables from {dotenv_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to load .env file: {str(e)}")
        return False

def main():
    print("Testing Azure Container Registry Access")
    print("-" * 50)
    
    # Try to load environment variables from .env file
    script_dir = Path(__file__).parent.absolute()
    dotenv_path = script_dir / '.env'
    if dotenv_path.exists():
        load_dotenv(dotenv_path)
    else:
        print(f"⚠️ No .env file found at {dotenv_path}")
        print("   You'll need to set environment variables manually")

    # Output locations of our resources
    print("Resource Locations:")
    print(f"- Function App Location: {os.environ.get('AZURE_LOCATION', 'Not specified')}")
    print(f"- Container Registry Location: {os.environ.get('REGISTRY_LOCATION', 'Not specified')}")
    print(f"- Static Web App Location: {os.environ.get('WEBAPP_LOCATION', 'Not specified')}")
    
    # Set default values for Azure Container Registry
    default_registry = "containerregistry2025.azurecr.io"
    default_image = f"{default_registry}/penguin-classifier:latest"
    registry_location = os.environ.get("REGISTRY_LOCATION", "North Europe")
    
    # Get values from environment with defaults
    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    resource_group = os.environ.get("AZURE_RESOURCE_GROUP")
    location = os.environ.get("AZURE_LOCATION", "North Europe")  # Default to North Europe
    container_image = os.environ.get("CONTAINER_IMAGE", default_image)
    registry_server = os.environ.get("REGISTRY_SERVER", default_registry)
    registry_username = os.environ.get("REGISTRY_USERNAME")
    registry_password = os.environ.get("REGISTRY_PASSWORD")
    
    # Check required environment variables
    required_vars = [
        "AZURE_SUBSCRIPTION_ID",
        "AZURE_RESOURCE_GROUP", 
        "REGISTRY_USERNAME",
        "REGISTRY_PASSWORD"
    ]
    
    missing_vars = []
    env_values = {
        "AZURE_LOCATION": location,
        "CONTAINER_IMAGE": container_image,
        "REGISTRY_SERVER": registry_server,
        "REGISTRY_LOCATION": registry_location,
        "WEBAPP_LOCATION": os.environ.get("WEBAPP_LOCATION", "West Europe")
    }
    
    for var in required_vars:
        value = os.environ.get(var)
        if not value:
            missing_vars.append(var)
        else:
            # Don't include sensitive values
            if "PASSWORD" in var or "KEY" in var:
                env_values[var] = "********"
            else:
                env_values[var] = value
    
    print("\nEnvironment Variable Check:")
    if missing_vars:
        print(f"❌ Missing required variables: {', '.join(missing_vars)}")
        for var in missing_vars:
            print(f"   - {var}: Not set")
    else:
        print("✅ All required environment variables are set")
    
    print("\nAvailable environment variables:")
    for var, value in env_values.items():
        print(f"   - {var}: {value}")
    
    if missing_vars:
        print("\n❌ Cannot proceed with authentication checks due to missing variables.")
        print("   Please set the required environment variables and try again.")
        return

    # Try Azure authentication
    print("\nTesting Azure Authentication:")
    try:
        print("Attempting to use DefaultAzureCredential...")
        credential = DefaultAzureCredential()
        token = credential.get_token("https://management.azure.com/.default")
        print("✅ DefaultAzureCredential authentication successful!")
    except Exception as auth_error:
        print(f"❌ DefaultAzureCredential failed: {str(auth_error)}")
        
        # Try AzureCliCredential as fallback
        try:
            print("\nAttempting to use AzureCliCredential as fallback...")
            cli_credential = AzureCliCredential()
            token = cli_credential.get_token("https://management.azure.com/.default")
            print("✅ AzureCliCredential authentication successful!")
            credential = cli_credential
        except Exception as cli_error:
            print(f"❌ AzureCliCredential also failed: {str(cli_error)}")
            print("\n❌ Cannot proceed with client initialization due to authentication failures.")
            return
    
    # Try initializing Container Instance client
    print("\nTesting Container Instance Client:")
    try:
        print(f"Initializing ContainerInstanceManagementClient for subscription {subscription_id}...")
        client = ContainerInstanceManagementClient(
            credential=credential,
            subscription_id=subscription_id
        )
        
        print("✅ Container Instance client initialized successfully!")
        
        # Try creating registry credential object
        print("\nTesting Container Registry Credentials:")
        try:
            print(f"Creating ImageRegistryCredential for registry {registry_server}...")
            registry_credential = ImageRegistryCredential(
                server=registry_server,
                username=registry_username,
                password=registry_password
            )
            print("✅ Registry credentials object created successfully!")
            
            # List container groups to test permissions
            print("\nTesting Container Instance API access:")
            try:
                print(f"Listing container groups in resource group {resource_group}...")
                container_groups = list(client.container_groups.list_by_resource_group(resource_group))
                print(f"✅ Successfully listed {len(container_groups)} container groups")
                
                # Print container groups for reference
                if (container_groups):
                    print("\nExisting container groups:")
                    for cg in container_groups:
                        print(f"   - {cg.name} (Status: {cg.provisioning_state})")
                else:
                    print("   No existing container groups found")
            except Exception as list_error:
                print(f"❌ Failed to list container groups: {str(list_error)}")
                
        except Exception as cred_error:
            print(f"❌ Failed to create registry credentials: {str(cred_error)}")
        
    except Exception as client_error:
        print(f"❌ Failed to initialize container client: {str(client_error)}")
    
    # Show region-specific advice
    print("\n📍 Region Analysis:")
    if "AZURE_LOCATION" in env_values and "REGISTRY_LOCATION" in env_values:
        function_location = env_values["AZURE_LOCATION"]
        registry_location = env_values["REGISTRY_LOCATION"]
        webapp_location = env_values["WEBAPP_LOCATION"]
        
        if function_location.lower() != registry_location.lower():
            print(f"⚠️  Your function ({function_location}) and registry ({registry_location}) are in different regions")
            print("   - Cross-region access can sometimes cause authentication or network issues")
            print("   - Consider ensuring Function and Container Registry are in the same region")
        else:
            print(f"✅ Your function and container registry are both in {function_location} - good!")
            
        if function_location.lower() != webapp_location.lower():
            print(f"ℹ️  Your function ({function_location}) and Static Web App ({webapp_location}) are in different regions")
            print("   - This is generally fine but could add minimal latency to API calls")
    
    # Try running a simple container to test full end-to-end
    bypass_container = os.environ.get("BYPASS_CONTAINER", "false").lower() == "true"
    if not bypass_container:
        print("\n🧪 Testing a quick container deployment:")
        try:
            # Real container test with Azure Container Instances
            test_features = [39.1, 18.7, 18.1, 37.5]
            print(f"Will attempt to classify penguin with features: {test_features}")
            print(f"This will use image: {container_image}")
            
            # Create a unique container name
            import uuid
            container_group_name = f"penguin-test-{uuid.uuid4().hex[:8]}"
            print(f"Creating container group: {container_group_name}")
            
            # Initialize the Container Instance client
            try:
                # Create credentials object and client
                credential = DefaultAzureCredential()
                container_client = ContainerInstanceManagementClient(
                    credential=credential,
                    subscription_id=subscription_id
                )
                
                print(f"✅ Successfully initialized Container Instance client")
                
                # Create registry credentials
                registry_credential = ImageRegistryCredential(
                    server=registry_server,
                    username=registry_username,
                    password=registry_password
                )
                
                from azure.mgmt.containerinstance.models import (
                    ContainerGroup, Container, ResourceRequirements, ResourceRequests,
                    EnvironmentVariable, ContainerGroupNetworkProtocol,
                    Port, IpAddress, ContainerGroupIpAddressType
                )
                
                # Prepare environment variables for the container
                env_vars = [ 
                    EnvironmentVariable(name="MODEL_PATH", value="/app/models/penguins_model.pkl"),
                    EnvironmentVariable(name="FEATURES", value=json.dumps(test_features)),
                    EnvironmentVariable(name="PYTHONUNBUFFERED", value="1")
                ]
                
                # Define container resources
                container_resource_requests = ResourceRequests(memory_in_gb=1.0, cpu=1.0)
                container_resources = ResourceRequirements(requests=container_resource_requests)
                
                # Define container
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
                
                # Create container group configuration
                container_group = ContainerGroup(
                    location=location,
                    containers=[container],
                    os_type="Linux",
                    restart_policy="Never",
                    image_registry_credentials=[registry_credential],
                    ip_address=group_ip_address
                )
                
                print(f"🚀 Deploying container group {container_group_name} in {resource_group}...")
                
                # Create the container group
                container_group_creation = container_client.container_groups.begin_create_or_update(
                    resource_group,
                    container_group_name,
                    container_group
                )
                
                # Wait for the container to complete
                print("⏳ Waiting for container deployment to complete...")
                container_group_result = container_group_creation.result()
                print(f"✅ Container group created: {container_group_result.name}")
                print(f"   Provisioning state: {container_group_result.provisioning_state}")
                
                # Get container logs for output
                import time
                print("⏳ Waiting for container to start and run (10 seconds)...")
                time.sleep(10)  # Wait a bit for the container to start and run
                
                print("📋 Retrieving container logs...")
                logs = container_client.containers.list_logs(
                    resource_group, 
                    container_group_name, 
                    "penguin-classifier-container"
                ).content
                
                print("\nContainer Logs:")
                print("-" * 40)
                print(logs)
                print("-" * 40)
                
                # Try to extract JSON output from container logs
                import re
                json_match = re.search(r'({.*})', logs)
                if json_match:
                    result_json = json_match.group(1)
                    prediction_result = json.loads(result_json)
                    print("\n✅ Successfully parsed result:")
                    print(json.dumps(prediction_result, indent=2))
                    
                    # Add human-readable species names if prediction exists
                    if "prediction" in prediction_result and prediction_result["prediction"] in (0, 1, 2):
                        penguin_species = ['Adelie', 'Chinstrap', 'Gentoo']
                        species_name = penguin_species[prediction_result['prediction']]
                        print(f"\n🐧 Penguin classification result: {species_name}")
                        print(f"   Confidence: {prediction_result.get('confidence', 'N/A')}")
                else:
                    print("\n❌ No valid JSON output found in container logs")
                
                # Clean up - delete the container group
                print(f"\n🧹 Cleaning up: Deleting container group {container_group_name}...")
                container_client.container_groups.begin_delete(resource_group, container_group_name)
                print("✅ Container group deletion initiated")
                
            except Exception as container_error:
                print(f"❌ Container deployment failed: {str(container_error)}")
        except Exception as e:
            print(f"❌ Container test failed: {str(e)}")
    else:
        print("\n🧪 BYPASS_CONTAINER is set to true - skipping container test")

if __name__ == "__main__":
    main()