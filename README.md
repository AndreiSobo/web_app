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
curl -X POST https://blue-wave-0b3a88b03.6.azurestaticapps.net/api/ClassifyPenguinSimple \
  -H "Content-Type: application/json" \
  -d '{"features": [47.5, 15.0, 21.7, 50.76]}'
```

## 🎯 **What This Project Does**

### **Purpose**
This project demonstrates end-to-end machine learning deployment using Azure cloud services. It classifies penguin species (Adelie, Chinstrap, or Gentoo) based on four physical measurements using a production-ready web application.

### **Key Features**
- **Real-time ML Predictions**: Instant species classification from penguin measurements
- **Cloud-Native Architecture**: Fully serverless deployment on Azure platform
- **Interactive Web Interface**: User-friendly form with immediate results display
- **Enterprise-Grade API**: RESTful endpoint for programmatic access

### **Input & Output**
- **Input**: Culmen length, culmen depth, flipper length, body mass (in mm/grams)
- **Output**: Species classification with confidence score and explainable AI insights
- **Performance**: <1 second response time, ~$0.001 per prediction

## 🏗️ **How It Works - Technical Implementation**

### **System Architecture & Data Flow**
```
User Input → Frontend Validation → HTTP Request → Azure Function → Pre-trained ML Model → JSON Response → Web Display
```

### **Step-by-Step Process**
1. **User Interaction**: User enters penguin measurements via web interface
2. **Data Processing**: JavaScript validates and normalizes input data 
3. **HTTP Trigger**: POST request sent to Azure Function endpoint (`/api/ClassifyPenguinSimple`)
4. **Model Inference**: Pre-trained Random Forest classifier processes the features
5. **Response Generation**: Function returns JSON with species prediction and confidence
6. **Result Display**: Web interface updates with classification results and explanations

### **Core Components**
1. **Frontend**: Azure Static Web App (HTML/CSS/JavaScript)
   - Responsive web interface for data input
   - Real-time form validation and user feedback
   - Interactive results display with explainable AI features

2. **Backend**: Azure Functions (Python 3.10) - **v2 Programming Model**
   - HTTP-triggered serverless function using blueprints and decorators
   - Cached pre-trained scikit-learn Random Forest model
   - JSON API with CORS support for cross-origin requests
   - Code-first approach eliminating `function.json` configuration files

3. **Machine Learning**: Random Forest Classifier
   - Pre-trained on Palmer Penguins dataset (>97% accuracy)
   - Cached in memory for fast inference (<100ms)
   - Handles 4 normalized features: culmen dimensions, flipper length, body mass

### **Technical Flow Details**
- **Model Loading**: Random Forest classifier loaded once and cached globally
- **Feature Processing**: Input normalized to match training data scaling
- **Prediction Pipeline**: Model inference → probability calculation → species mapping
- **Response Format**: Structured JSON with prediction, confidence, and metadata

## 🚀 **Live Deployment & Access**

### **Live Application**
- **Web Interface**: https://blue-wave-0b3a88b03.6.azurestaticapps.net/
- **API Endpoint**: https://blue-wave-0b3a88b03.6.azurestaticapps.net/api/ClassifyPenguinSimple

### **Azure Resources**
- **Static Web App**: Hosts frontend and routes API calls
- **Function App**: Processes ML predictions
- **Application Insights**: Monitors performance and errors

## 📁 **Project Structure**

```
web_app/
├── static/                    # Frontend web application
│   ├── index.html            # Main web interface
│   ├── app.js               # Frontend logic and API calls
│   └── styles.css           # Styling and responsive design
├── function_app/             # Azure Functions backend (v2 programming model)
│   ├── __init__.py          # Main app with blueprint registration
│   ├── function_app.py      # Entry point for v2 model
│   ├── host.json           # Host configuration with v2 extension bundle
│   ├── requirements.txt    # Python dependencies
│   └── ClassifyPenguinSimple/
│       ├── __init__.py     # Function blueprint with decorators
│       └── penguins_model.pkl  # Pre-trained ML model
├── models/                   # ML model files
├── notebooks/               # Data science workflows
├── data/                    # Training data
└── documentation/           # Technical documentation
```

**Key v2 Programming Model Features:**
- No `function.json` files required
- Function configuration via Python decorators
- Blueprint-based organization
- Centralized app registration

## 🧪 **Testing**

### **Production Testing**

#### **Web Interface**
1. Visit: https://blue-wave-0b3a88b03.6.azurestaticapps.net/
2. Enter penguin measurements or use the "Use Values" buttons
3. Click "Classify Penguin Species" to see prediction results

#### **API Testing**
```bash
curl -X POST https://blue-wave-0b3a88b03.6.azurestaticapps.net/api/ClassifyPenguinSimple \
  -H "Content-Type: application/json" \
  -d '{"features": [39.1, 18.7, 18.1, 37.5]}'
```

### **Local Development Testing**

#### **Starting the Function Runtime**
For local testing, the Azure Functions runtime needs to run in the background. Use this command:

```bash
cd /home/andrei/git/web_app/function_app && nohup func host start > /tmp/func.log 2>&1 & sleep 3 && echo "Function started, testing now..."
```

**Why this command works:**
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
To stop the background function:
```bash
lsof -ti:7071 | xargs kill -9
```

#### **Common Issues**
- **Connection refused**: Function not started or still initializing - wait a few seconds
- **Port already in use**: Kill existing processes with the stop command above
- **Import errors**: Ensure virtual environment is activated and dependencies installed

Expected output:
```json
{"prediction": 0, "species_name": "Adelie", "confidence": 0.98, "success": true}
```

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

## 🛠️ **Development & Deployment**

### **Quick Start for Developers**
```bash
# Clone and setup
git clone https://github.com/AndreiSobo/web_app.git
cd web_app

# Local development with v2 programming model
cd function_app
source ../web_app_env/bin/activate  # Activate virtual environment
func host start                      # Start Azure Functions locally (v2 model)

# In another terminal
cd static && python -m http.server   # Serve static files
```

**Note**: This project uses Azure Functions **v2 Programming Model** which uses decorators and blueprints instead of `function.json` configuration files.

### **Deployment**
- **Automatic**: Push to GitHub triggers auto-deployment via GitHub Actions
- **Manual**: Deploy via Azure CLI or VS Code Azure extensions

For detailed technical implementation, see **[Technical Documentation](documentation/TECHNICAL_OVERVIEW.md)**

## 📚 **Documentation**

### **Additional Documentation**
- **[Technical Overview](documentation/TECHNICAL_OVERVIEW.md)** - Complete system architecture, API reference, and implementation details for academic/professional presentations

## 🎯 **Why This Project Matters - Showcase Objectives**

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
- **Performance Optimization**: <1 second response times with cold start management
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
- **Cost Optimization**: Choosing appropriate Azure services for workload requirements
- **Developer Experience**: Local development workflow with cloud deployment automation

This project serves as a practical example of how to leverage Azure's cloud infrastructure to deploy machine learning models in a production-ready, cost-effective, and scalable manner.

## 🤝 **Contributing**

Feel free to submit issues and enhancement requests. This project serves as a learning example for ML deployment on Azure.

## 📄 **License**

This project is open source and available under the [MIT License](LICENSE).

---

**Built with ❤️ using Azure, Python, and Machine Learning**
