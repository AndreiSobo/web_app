# 🐧 Penguin Species Classifier

A machine learning web application that classifies penguin species based on physical measurements using a Random Forest model deployed on Azure.

## 🚀 **Quick Start**

**Live Demo**: [https://blue-wave-0b3a88b03.6.azurestaticapps.net/](https://blue-wave-0b3a88b03.6.azurestaticapps.net/)

### **✨ New Features**
- **Species Reference Values**: Click-to-fill average measurements for each penguin species
- **Explainable AI Analysis**: SHAP-based feature importance explanations for predictions
- **Plan A+ Architecture**: Decoupled frontend and backend services for enhanced scalability

**Species Reference Data:**
- **Adelie**: Culmen 38.8×18.3mm, Flipper 190mm, Mass 3701g
- **Chinstrap**: Culmen 47.5×15.0mm, Flipper 217mm, Mass 5076g  
- **Gentoo**: Culmen 48.8×18.4mm, Flipper 196mm, Mass 3733g

### **Test the API Directly**
```bash
# Test with Chinstrap penguin averages (Plan A+ direct function endpoint)
curl -X POST https://penguin-classifier-consumption-dngqgqbga0g2eqgy.northeurope-01.azurewebsites.net/api/ClassifyPenguinSimple \
  -H "Content-Type: application/json" \
  -d '{"features": [47.5, 15.0, 217, 5076]}'
```

## 🎯 **What This Project Does**

### **Purpose**
This project demonstrates end-to-end machine learning deployment using Azure cloud services. It classifies penguin species (Adelie, Chinstrap, or Gentoo) based on four physical measurements using a production-ready web application.

### **Key Features**
- **Real-time ML Predictions**: Instant species classification from penguin measurements
- **Explainable AI**: SHAP-based feature importance analysis showing prediction reasoning
- **Plan A+ Architecture**: Decoupled Static Web App frontend + dedicated Functions App backend
- **Interactive Web Interface**: User-friendly form with immediate results and XAI insights
- **Enterprise-Grade API**: RESTful endpoints with full ML and XAI capabilities

### **Input & Output**
- **Input**: Culmen length, culmen depth, flipper length, body mass (in mm/grams)
- **Output**: Species classification with confidence score, feature importance analysis, and SHAP explanations

## 🏗️ **How It Works - Technical Implementation**

### **System Architecture & Data Flow (Plan A+)**
```
User Input → Frontend (Static Web App) → Direct API Call → Azure Functions App → ML Model + XAI Analysis → JSON Response → Web Display
```

### **Step-by-Step Process**
1. **User Interaction**: User enters penguin measurements via web interface
2. **Data Processing**: JavaScript validates input data 
3. **Direct API Call**: POST request sent to dedicated Azure Functions App endpoint
4. **ML Inference**: Pre-trained Random Forest classifier processes the features
5. **XAI Analysis**: Internal call to SHAP-based XAI function for feature importance
6. **Response Generation**: Combined JSON with species prediction, confidence, and SHAP explanations
7. **Result Display**: Web interface updates with classification results and explainable AI analysis

### **Core Components (Plan A+ Architecture)**
1. **Frontend**: Azure Static Web App (HTML/CSS/JavaScript)
   - Responsive web interface with dark/light mode support
   - Real-time form validation and species reference data
   - Interactive results display with collapsible XAI explanations

2. **Backend**: Dedicated Azure Functions App (Python 3.10) 
   - **ClassifyPenguinSimple**: Main prediction endpoint with integrated XAI calls
   - **XAI Function**: SHAP-based explainable AI analysis endpoint
   - Full ML library support (1.5GB limit vs 100MB Static Web App limit)
   - CORS-enabled for cross-origin requests from Static Web App

3. **Machine Learning & AI**: 
   - **Random Forest Classifier**: Pre-trained model (>97% accuracy) with memory caching
   - **SHAP Explainable AI**: TreeExplainer providing feature importance analysis
   - **Background Object**: Pre-computed reference data for SHAP calculations

### **Technical Flow Details**
- **Model Loading**: Random Forest classifier loaded once and cached globally
- **Feature Processing**: Input normalized to match training data scaling
- **Prediction Pipeline**: Model inference → probability calculation → species mapping
- **Response Format**: Structured JSON with prediction, confidence, and metadata

## 🚀 **Live Deployment & Access**

### **Live Application**
- **Web Interface**: https://blue-wave-0b3a88b03.4.azurestaticapps.net/
- **API Endpoints**: 
  - **Main Classification**: https://penguin-classifier-consumption-dngqgqbga0g2eqgy.northeurope-01.azurewebsites.net/api/ClassifyPenguinSimple
  - **XAI Analysis**: https://penguin-classifier-consumption-dngqgqbga0g2eqgy.northeurope-01.azurewebsites.net/api/XAI

### **Azure Resources (Plan A+)**
- **Static Web App**: Hosts frontend only (static files)
- **Dedicated Functions App**: Processes ML predictions and XAI analysis
- **Application Insights**: Monitors performance and errors

## 🧪 **Testing**

### **Production Testing**

#### **Web Interface**
1. Visit: https://blue-wave-0b3a88b03.6.azurestaticapps.net/
2. Enter penguin measurements or use the "Use Values" buttons
3. Click "Classify Penguin Species" to see prediction results

#### **API Testing**
```bash
# Test main classification with XAI integration
curl -X POST https://penguin-classifier-consumption-dngqgqbga0g2eqgy.northeurope-01.azurewebsites.net/api/ClassifyPenguinSimple \
  -H "Content-Type: application/json" \
  -d '{"features": [39.1, 18.7, 181, 3750]}'

# Expected response includes XAI analysis:
# {"prediction": 0, "species_name": "Adelie", "confidence": 0.52, "top_features": [{"name": "culmen-length", "impact": 0.2654}, {"name": "flipper-length", "impact": -0.1852}]}
```

### **Local Development Testing**

#### **Starting the Function Runtime**
For local testing, the Azure Functions runtime needs to run in the background. Use this command:

```bash
cd /home/andrei/git/web_app/function_app && nohup func host start > /tmp/func.log 2>&1 & sleep 3 && echo "Function started, testing now..."
```

**How this command works:**
- `nohup` - Prevents process termination when terminal closes
- `func host start` - Starts the Azure Functions runtime
- `> /tmp/func.log 2>&1` - Redirects output to log file for debugging
- `&` - Runs in background, freeing up terminal
- `sleep 3` - Allows runtime to fully initialize before testing

#### **Testing Local Function**
Once the function is running, test with curl:

```bash
curl -X POST http://localhost:7071/api/ClassifyPenguinSimple \
  -H "Content-Type: application/json" \
  -d '{"features": [39.1, 18.7, 18.1, 37.5]}'
```

#### **Checking Function Logs**
Monitor the function output:
```bash
tail -f /tmp/func.log
```

#### **Stopping Local Function**
To stop the background function or any process that uses this port:
```bash
lsof -ti:7071 | xargs kill -9
```

#### **Common Issues**
- **Connection refused**: Function not started or still initializing - wait a few seconds
- **Port already in use**: Kill existing processes with the stop command above
- **Import errors**: Ensure virtual environment is activated and dependencies installed

Expected output:
```json
{"prediction": 0, "species_name": "Adelie", "confidence": 0.52, "success": true, "top_features": [{"name": "culmen-length", "impact": 0.2654}, {"name": "flipper-length", "impact": -0.1852}]}
```

## 📈 **Performance & Costs**

### **Performance Metrics**
- **Response Time**: <1 second
- **Availability**: 99.9% (Azure SLA)
- **Throughput**: Scales automatically with demand
- **Cold Start**: ~10 seconds for first request

### **Cost Analysis**
- **Function Execution**: ~$0.001 per prediction
- **Static Web App**: Free tier sufficient
- **Data Transfer**: Negligible for API responses
- **Monthly Estimate**: <$5 for moderate usage


## 🛠️ **Development & Deployment**

### **Quick Start for Developers**
```bash
# Clone and setup
git clone https://github.com/AndreiSobo/web_app.git
cd web_app

# create and activate virtual env
python3 -m venv new_venv_name
source new_venv_name/bin/activate

# Local development with v2 programming model
cd function_app
source ../web_app_env/bin/activate  # Activate virtual environment
func host start                      # Start Azure Functions locally (v2 model)

# In another terminal
cd static && python -m http.server   # Serve static files
```

### **Deployment**
- **Manual**: Deploy via Azure CLI or VS Code Azure extensions. This project was deployed using the CLI

For detailed technical implementation, see **[Technical Documentation](documentation/TECHNICAL_OVERVIEW.md)**

## 📚 **Documentation**

### **Additional Documentation**
- **[Technical Overview](documentation/TECHNICAL_OVERVIEW.md)** - Complete system architecture, API reference, and implementation details

## 🎯 **Why This Project Matters**

### **Cloud Infrastructure Demonstration**
This project showcases modern cloud-native architecture patterns:
- **Serverless Computing**: Azure Functions eliminate infrastructure management overhead
- **Static Web Apps**: Cost-effective frontend hosting with integrated CI/CD
- **Auto-Scaling**: Platform handles traffic spikes automatically without configuration
- **Pay-per-Use Model**: Only pay for actual function executions (~$0.001 per prediction)

### **Machine Learning Best Practices**
Demonstrates production ML deployment techniques:
- **Model Serving**: Efficient in-memory caching of pre-trained models
- **API Design**: RESTful endpoints with proper error handling and validation
- **Performance Optimization**: <1 second response times after cold start
- **Explainable AI**: Feature importance and confidence scoring for transparency

### **Azure Platform Integration**
Exhibits comprehensive Azure ecosystem usage:
- **Azure Static Web Apps**: Seamless frontend deployment with GitHub integration
- **Azure Functions**: Serverless compute for ML inference workloads
- **Application Insights**: Built-in monitoring and performance analytics
- **DevOps Integration**: Automated deployment pipelines via GitHub Actions

### **End-to-End Solution Architecture**
Showcases complete cloud solution development:
- **Full-Stack Development**: Frontend, backend, and ML model integration
- **Production Readiness**: Error handling, CORS configuration, and scalability
- **Cost Optimization**: Choosing appropriate Azure services to keep costs low

This project demonstrates how to leverage Azure's cloud infrastructure to deploy machine learning models in a production-ready, cost-effective, and scalable manner. Using the webpage for user input bridges the gap between individuals not familiar with machine learning and the benefits of using these models. 

## 🚀 **Deployment**

### **Azure Function Deployment**

**Recommended Method: Azure CLI Direct Deployment**

Due to authentication challenges with GitHub Actions in educational Azure accounts, we recommend using Azure CLI for function deployment:

```bash
# 1. Install Azure CLI (if not already installed)
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# 2. Login to Azure
az login  # leads to a browser for Microsoft Authentication

# 3. Navigate to function directory and deploy
cd function_app
func azure functionapp publish penguin-classifier-consumption
```

**What the deployment does:**
- Authenticates using your Azure CLI session
- Performs remote build on Azure infrastructure
- Installs Python dependencies from requirements.txt
- Compresses and uploads function code
- Configures function triggers and bindings
- Activates the deployed function

### **Static Web App Deployment**

The frontend is automatically deployed via GitHub Actions when changes are pushed to the master branch. The workflow file `azure-static-web-apps-blue-wave-0b3a88b03.yml` handles this process.

### **Deployment Architecture**

```
Frontend (Static Web App) → Direct API Call → Azure Function → ML Model → Response
```

**Note**: This project bypasses the typical Static Web App + Function integration due to deployment authentication issues, instead using direct function URLs in production.

For detailed deployment troubleshooting and alternatives, see [`documentation/TECHNICAL_OVERVIEW.md`](documentation/TECHNICAL_OVERVIEW.md#-deployment-strategies-and-lessons-learned).

## 🤝 **Contributing**

Feel free to submit issues and enhancement requests. This project serves as a learning example for ML deployment on Azure.

## 📄 **License**

This project is open source and available under the [MIT License](LICENSE).

---

**Built with ❤️ using Azure, Python, and Machine Learning**
