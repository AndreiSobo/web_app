# 🐧 Penguin Species Classifier

A machine learning web application that classifies penguin species based on physical measurements using a Random Forest model deployed on Azure.

## 🚀 **Quick Start**

**Live Demo**: [https://blue-wave-0b3a88b03.6.azurestaticapps.net/](https://blue-wave-0b3a88b03.6.azurestaticapps.net/)

### **✨ New Feature: Species Reference Values**
The web interface now includes average measurements for each penguin species:
- **Adelie**: Culmen 38.8×18.3mm, Flipper 190mm, Mass 3701g
- **Chinstrap**: Culmen 47.5×15.0mm, Flipper 217mm, Mass 5076g  
- **Gentoo**: Culmen 48.8×18.4mm, Flipper 196mm, Mass 3733g

Click "Use Values" buttons to quickly test with realistic species data!

### **Test the API Directly**
```bash
# Test with Chinstrap penguin averages
curl -X POST https://penguin-classifier-function.azurewebsites.net/api/classifypenguinsimple \
  -H "Content-Type: application/json" \
  -d '{"features": [47.5, 15.0, 21.7, 50.76]}'
```

## 🎯 **Project Overview**

### **Purpose**
This project demonstrates end-to-end machine learning deployment using Azure cloud services. It predicts penguin species (Adelie, Chinstrap, or Gentoo) based on four physical measurements.

### **Goals**
- **Educational**: Showcase modern ML deployment practices
- **Technical**: Demonstrate Azure Functions, Static Web Apps, and ML integration
- **Portfolio**: Exhibit cloud development and machine learning skills

### **Scope**
- **Input**: Culmen length, culmen depth, flipper length, body mass
- **Output**: Species classification with confidence score
- **Technology Stack**: Python, scikit-learn, Azure Functions, Azure Static Web Apps
- **Response Time**: <1 second
- **Cost**: ~$0.001 per prediction

## 🏗️ **Architecture**

### **Current Architecture (Simplified)**
```
┌─────────────────┐    ├── HTTPS ──┤    ┌──────────────────┐    ├── ML ─┤    ┌─────────────┐
│   Web Browser   │ ── │  Request  │ ── │ Azure Function   │ ── │ Model │ ── │ Prediction  │
│  (Static App)   │    │           │    │ (Python 3.9)     │    │       │    │  Response   │
└─────────────────┘    └───────────┘    └──────────────────┘    └───────┘    └─────────────┘
```

### **Components**
1. **Frontend**: Azure Static Web App (HTML/CSS/JavaScript)
2. **Backend**: Azure Functions (Python)
3. **Model**: Random Forest Classifier (scikit-learn)
4. **Data Flow**: Direct function-to-model integration

### **Previous Architecture (Discarded)**
Initially explored Docker containerization with Azure Container Instances, but this approach was abandoned due to:
- **High Costs**: ~$0.50+ per prediction vs ~$0.001
- **Slow Response**: 2-5 minutes vs <1 second  
- **Complexity**: Multiple failure points vs single endpoint
- **Resource Overhead**: Container creation/destruction vs cached model

## 📊 **Machine Learning Model**

### **Model Details**
- **Algorithm**: Random Forest Classifier
- **Features**: 4 numerical inputs (normalized)
- **Classes**: 3 penguin species (0=Adelie, 1=Chinstrap, 2=Gentoo)
- **Training Data**: Palmer Penguins dataset
- **Model File**: `penguins_model.pkl` (268KB)

### **Feature Engineering**
- **Culmen Length**: Raw millimeters (e.g., 39.1mm)
- **Culmen Depth**: Raw millimeters (e.g., 18.7mm)
- **Flipper Length**: Normalized by 10 (181mm → 18.1)
- **Body Mass**: Normalized by 100 (3750g → 37.5)

## 🚀 **Deployment**

### **Live Application**
- **Web Interface**: https://blue-wave-0b3a88b03.6.azurestaticapps.net/
- **API Endpoint**: https://penguin-classifier-function.azurewebsites.net/api/classifypenguinsimple

### **Azure Resources**
- **Static Web App**: Hosts frontend and routes API calls
- **Function App**: Processes ML predictions
- **Application Insights**: Monitors performance and errors

## 📁 **Project Structure**

```
web_app/
├── static/                          # Frontend application
│   ├── index.html                   # Main web interface
│   ├── app.js                       # JavaScript logic & API calls
│   ├── styles.css                   # Styling
│   └── images/                      # UI assets
├── function_app/                    # Azure Functions backend
│   ├── ClassifyPenguinSimple/       # Main prediction function
│   │   ├── __init__.py              # Function logic
│   │   ├── function.json            # Azure Functions configuration
│   │   └── penguins_model.pkl       # ML model file
│   ├── DebugEndpoint/               # Health check function
│   ├── host.json                    # Functions host configuration
│   └── requirements.txt             # Python dependencies
├── models/                          # Model development
│   └── penguins_model.pkl           # Trained model
├── notebooks/                       # Data science workflows
├── data/                            # Training data
├── staticwebapp.config.json         # Static Web App routing
└── documentation/                   # Additional docs
```

## 🔧 **Technical Implementation**

### **Azure Function: ClassifyPenguinSimple**

**Purpose**: Receives HTTP requests with penguin measurements and returns species predictions.

**Key Features**:
- **Model Caching**: Loads model once on cold start, caches for subsequent requests
- **Error Handling**: Comprehensive validation and error responses
- **CORS Support**: Allows cross-origin requests from web interface
- **Fast Response**: <1 second prediction time

**Input Format**:
```json
{
  "features": [39.1, 18.7, 18.1, 37.5]
}
```

**Output Format**:
```json
{
  "prediction": 0,
  "class": "Adelie",
  "species_name": "Adelie", 
  "features": [39.1, 18.7, 18.1, 37.5],
  "success": true,
  "confidence": 0.98
}
```

**Function Workflow**:
1. **Request Validation**: Checks for 4 numerical features
2. **Model Loading**: Retrieves cached model or loads from file
3. **Prediction**: Applies model to input features
4. **Response Formatting**: Returns JSON with prediction and metadata

### **Web Interface**

**Purpose**: Provides user-friendly form for entering penguin measurements.

**Key Features**:
- **Input Validation**: Ensures proper data types and ranges
- **Data Normalization**: Converts raw measurements to model format
- **Error Handling**: Tries multiple API endpoints with fallbacks
- **Debug Mode**: Shows detailed API responses for troubleshooting

**User Flow**:
1. Enter measurements in intuitive units (mm, grams)
2. JavaScript normalizes data for model compatibility
3. API call to Azure Function with formatted data
4. Display species prediction with confidence score

### **Static Web App Configuration**

**Purpose**: Routes API calls and serves static content.

**Key Features**:
- **API Routing**: Maps `/api/*` to Azure Functions
- **CORS Headers**: Enables cross-origin requests
- **Fallback Routing**: Handles single-page application navigation

## 🧪 **Testing**

### **Function Testing**
```bash
# Test API endpoint directly
curl -X POST https://penguin-classifier-function.azurewebsites.net/api/classifypenguinsimple \
  -H "Content-Type: application/json" \
  -d '{"features": [39.1, 18.7, 18.1, 37.5]}'
```

### **Web Interface Testing**
1. Navigate to web application
2. Enter sample measurements:
   - Culmen Length: 39.1mm
   - Culmen Depth: 18.7mm  
   - Flipper Length: 181mm (normalized to 18.1)
   - Body Mass: 3750g (normalized to 37.5)
3. Verify "Adelie" prediction with high confidence

## 📈 **Performance & Costs**

### **Performance Metrics**
- **Response Time**: <1 second
- **Availability**: 99.9% (Azure SLA)
- **Throughput**: Scales automatically with demand
- **Cold Start**: <5 seconds for first request

### **Cost Analysis**
- **Function Execution**: ~$0.001 per prediction
- **Static Web App**: Free tier sufficient
- **Data Transfer**: Negligible for API responses
- **Monthly Estimate**: <$10 for moderate usage

## 🚀 **Future Enhancements**

### **Short Term**
- **Model Retraining**: Update with new penguin data
- **Additional Features**: Add penguin sex prediction
- **UI Improvements**: Better visualization of results

### **Long Term**
- **Image Classification**: Migrate to computer vision for penguin photos
- **Container Deployment**: For larger models requiring GPU support
- **Multi-Model Pipeline**: Combine multiple ML models for enhanced accuracy

## 🛠️ **Development Setup**

### **Prerequisites**
- Python 3.8+ with virtual environment
- Azure CLI
- Azure Functions Core Tools
- VS Code with Azure extensions

### **Local Development**
```bash
# Clone repository
git clone https://github.com/AndreiSobo/web_app.git
cd web_app

# Set up Python environment
python -m venv web_app_env
source web_app_env/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Run Azure Functions locally
cd function_app
func host start
```

### **Deployment**
1. **Function App**: Deploy via VS Code Azure Functions extension
2. **Static Web App**: Auto-deploys from GitHub repository
3. **Configuration**: Set up routing in `staticwebapp.config.json`

## 📚 **Documentation**

### **Additional Documentation**
- **[Technical Overview](documentation/TECHNICAL_OVERVIEW.md)** - Complete system architecture, API reference, and implementation details for academic/professional presentations

### **Learning Outcomes**

This project demonstrates:
- **Cloud Architecture**: Serverless computing with Azure Functions
- **Machine Learning Deployment**: Production ML model serving
- **Web Development**: Modern JavaScript and responsive design
- **DevOps**: CI/CD with GitHub and Azure integration
- **Cost Optimization**: Choosing appropriate cloud services for workload

## 🤝 **Contributing**

Feel free to submit issues and enhancement requests. This project serves as a learning example for ML deployment on Azure.

## 📄 **License**

This project is open source and available under the [MIT License](LICENSE).

---

**Built with ❤️ using Azure, Python, and Machine Learning**
