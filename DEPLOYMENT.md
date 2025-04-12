# Penguin Classifier - Deployment Guide

This document describes how to deploy the Penguin Classifier web application and its Azure-based infrastructure.

## Architecture Overview

The solution consists of three main components:

1. **Flask Web Application**: A web interface where users enter penguin measurements
2. **Azure Function**: Handles requests from the web app and triggers the container instance
3. **Container Instance**: Runs your trained penguin classifier model and returns predictions

## Prerequisites

- Azure subscription
- Azure CLI installed
- Docker installed for local testing
- Python 3.9+

## Environment Variables

### For local testing:

Create a `.env` file in the project root with these variables:

```
# For direct testing without Azure
USE_DIRECT_CONNECTION=true
CONTAINER_URL=http://localhost:5000/predict
FLASK_DEBUG=true
PORT=8080

# For Azure deployment
AZURE_FUNCTION_URL=https://your-function-app-name.azurewebsites.net/api/ClassifyPenguin
```

### For the Azure Function:

Configure these application settings in your Azure Function:

```
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_RESOURCE_GROUP=your-resource-group
AZURE_LOCATION= North Europe
CONTAINER_IMAGE=your-registry.azurecr.io/penguin-classifier:latest
REGISTRY_SERVER=your-registry.azurecr.io
REGISTRY_USERNAME=your-username
REGISTRY_PASSWORD=your-password
```

## Deployment Steps

### 1. Build and Push the Docker Image

Update the Dockerfile to include the classify-only mode:

```bash
# Build the Docker image
docker build -t penguin-classifier .

# Tag the image for your container registry
docker tag penguin-classifier your-registry.azurecr.io/penguin-classifier:latest

# Push to container registry
docker push your-registry.azurecr.io/penguin-classifier:latest
```

### 2. Deploy the Azure Function

```bash
# Create a function app
az functionapp create \
  --name your-function-app-name \
  --storage-account your-storage-account \
  --consumption-plan-location eastus \
  --resource-group your-resource-group \
  --runtime python \
  --runtime-version 3.9 \
  --functions-version 4

# Deploy the function code
cd path/to/function
func azure functionapp publish your-function-app-name
```

### 3. Deploy the Flask Web App (Azure App Service)

```bash
# Create an app service plan
az appservice plan create \
  --name penguin-web-plan \
  --resource-group your-resource-group \
  --sku B1 \
  --is-linux

# Create a web app
az webapp create \
  --resource-group your-resource-group \
  --plan penguin-web-plan \
  --name your-web-app-name \
  --runtime "PYTHON|3.9" \
  --deployment-source-url https://github.com/your-username/your-repo.git \
  --deployment-source-branch main

# Configure environment variables
az webapp config appsettings set \
  --resource-group your-resource-group \
  --name your-web-app-name \
  --settings AZURE_FUNCTION_URL=https://your-function-app-name.azurewebsites.net/api/ClassifyPenguin
```

### 4. Deploy as Static Web App (Alternative)

For a static web app with Azure Functions backend:

```bash
# Install Azure Static Web Apps CLI
npm install -g @azure/static-web-apps-cli

# Deploy
swa deploy \
  --app-name your-static-web-app \
  --resource-group your-resource-group \
  --api-location ./src \
  --app-location ./static \
  --output-location ./static
```

## Testing the Deployment

1. Open your web app URL: `https://your-web-app-name.azurewebsites.net/`
2. Enter penguin measurements
3. Click "Classify Penguin Species"

## Troubleshooting

- Check Azure Function logs: `az functionapp log tail --name your-function-app-name --resource-group your-resource-group`
- Check Web App logs: `az webapp log tail --name your-web-app-name --resource-group your-resource-group`
- Test container locally: `docker run -p 5000:5000 -e MODEL_PATH=/app/models/penguins_model.pkl penguin-classifier`