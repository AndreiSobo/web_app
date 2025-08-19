# Penguin Classifier - Deployment Guide

This document describes how to deploy the Penguin Species Classifier web application using the simplified Azure Functions architecture.

## 🏗️ **Architecture Overview**

The solution consists of two main components:

1. **Azure Static Web App**: Frontend interface where users enter penguin measurements
2. **Azure Function**: Serverless backend that processes requests and returns species predictions

**Previous Architecture**: Initially explored Docker containerization with Azure Container Instances, but this approach was discarded due to high costs (~$0.50+ per prediction), slow response times (2-5 minutes), and unnecessary complexity for lightweight ML inference.

**Current Architecture**: Simplified serverless approach using Azure Functions with embedded ML model, achieving <1 second response times and ~$0.001 per prediction cost.

## 📋 **Prerequisites**

- Azure subscription with active billing
- Azure CLI installed and configured
- Azure Functions Core Tools v4
- Python 3.9+ for local development
- Git for source control

## 🚀 **Deployment Steps**

### **1. Deploy the Azure Function**

```bash
# Navigate to function directory
cd function_app

# Install dependencies locally (optional, for testing)
pip install -r requirements.txt

# Deploy to Azure (requires Azure Functions Core Tools)
func azure functionapp publish penguin-classifier-function

# Or use Azure CLI
az functionapp deployment source config \
  --name penguin-classifier-function \
  --resource-group your-resource-group \
  --repo-url https://github.com/your-username/web_app.git \
  --branch master \
  --manual-integration
```

### **2. Deploy the Static Web App**

```bash
# Option A: Deploy via GitHub Actions (recommended)
# Push to GitHub and Azure Static Web Apps will auto-deploy

# Option B: Deploy using Azure CLI
az staticwebapp create \
  --name penguin-classifier-web \
  --resource-group your-resource-group \
  --source https://github.com/your-username/web_app.git \
  --location "West US 2" \
  --branch master \
  --app-location "/static" \
  --api-location "/function_app"
```

### **3. Configure Static Web App Routing**

The `staticwebapp.config.json` file is already configured to route API calls to the Azure Function:

```json
{
  "routes": [
    {
      "route": "/api/classifypenguinsimple",
      "methods": ["POST"],
      "rewrite": "/api/ClassifyPenguinSimple"
    }
  ]
}
```

## 🧪 **Testing the Deployment**

### **Test the Azure Function directly:**
```bash
curl -X POST https://your-function-app.azurewebsites.net/api/classifypenguinsimple \
  -H "Content-Type: application/json" \
  -d '{"features": [39.1, 18.7, 18.1, 37.5]}'
```

### **Test the Static Web App:**
Visit your deployed URL and enter penguin measurements through the web interface.

### **Expected Response:**
```json
{
  "prediction": 0,
  "species_name": "Adelie",
  "confidence": 1.0,
  "features": [39.1, 18.7, 1.81, 0.375],
  "success": true
}
```

## 🔧 **Local Development**

### **Run the Function Locally:**
```bash
cd function_app
func start
```

### **Serve Static Files Locally:**
```bash
# Use Python's built-in server
cd static
python -m http.server 8000

# Or use Node.js live-server
npx live-server static
```

## 📊 **Monitoring and Logs**

### **Azure Function Logs:**
```bash
# View real-time logs
func azure functionapp logstream penguin-classifier-function

# Or use Azure Portal -> Function App -> Monitor
```

### **Static Web App Logs:**
Access through Azure Portal -> Static Web Apps -> your-app -> Functions

## 🛠️ **Troubleshooting**

### **Common Issues:**

1. **Function not responding:**
   - Check that the model file `penguins_model.pkl` is included in the function directory
   - Verify Python dependencies in `requirements.txt`
   - Check function logs in Azure Portal

2. **CORS issues:**
   - Ensure CORS is properly configured in the function
   - Check that the Static Web App can access the function URL

3. **Static Web App routing:**
   - Verify `staticwebapp.config.json` is in the root directory
   - Check that API routes are correctly configured

### **Useful Commands:**
- Check function status: `func azure functionapp list-functions penguin-classifier-function`
- Restart function app: `az functionapp restart --name penguin-classifier-function --resource-group your-resource-group`
- View deployment history: Check GitHub Actions or Azure DevOps pipeline

## 💰 **Cost Optimization**

### **Azure Functions Pricing:**
- **Consumption Plan**: Pay per execution (~$0.001 per prediction)
- **Typical monthly cost**: $5-20 for moderate usage
- **Free tier**: 1M executions and 400,000 GB-seconds per month

### **Static Web Apps Pricing:**
- **Free tier**: 100GB bandwidth, custom domains
- **Standard tier**: $9/month for additional features

### **Total Estimated Cost:**
- **Development/Testing**: $0-5/month (free tiers)
- **Production**: $10-30/month depending on usage

---

**🎯 Result**: Fast, cost-effective, and scalable penguin species classification service using modern serverless architecture!
