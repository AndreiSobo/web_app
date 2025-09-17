# 🐧 Penguin Species Classifier

A machine learning web application that classifies penguin species based on physical measurements using a Random Forest model deployed on Azure.

## 🚀 **Quick Start**

**Live Demo**: [https://blue-wave-0b3a88b03.6.azurestaticapps.net/](https://blue-wave-0b3a88b03.6.azurestaticapps.net/)


## 🎯 **What This Project Does**

### **Purpose**
This project demonstrates end-to-end machine learning deployment using Azure cloud services. It classifies penguin species (Adelie, Chinstrap, or Gentoo) based on four physical measurements using a production-ready web application.

### **Key Features**
- **Real-time ML Predictions**: Instant species classification from penguin measurements
- **Explainable AI**: SHAP-based feature importance analysis showing prediction reasoning
- **Architecture**: Decoupled Static Web App frontend + dedicated Functions App backend
- **Interactive Web Interface**: User-friendly form with immediate results and XAI insights
- **Enterprise-Grade API**: RESTful endpoints with full ML and XAI capabilities

### **Input & Output**
- **Input**: Culmen length, culmen depth, flipper length, body mass (in mm/grams)
- **Output**: Species classification with confidence score, feature importance analysis, and SHAP explanations

## 🏗️ **How It Works - Technical Implementation**

### **System Architecture & Data Flow**
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

### **Core Components**
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
- **Monthly Estimate**: <$5 for moderate usage, usually under $1


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

This project demonstrates how to leverage Azure's cloud infrastructure to deploy machine learning models in a production-ready, cost-effective, and scalable manner. The simplicity of the website serves to bridge the gap between individuals not familiar with machine learning and the benefits of using these models. 


For detailed deployment troubleshooting and alternatives, see [`documentation/TECHNICAL_OVERVIEW.md`](documentation/TECHNICAL_OVERVIEW.md#-deployment-strategies-and-lessons-learned).

## 🤝 **Contributing**

Feel free to submit issues and enhancement requests. This project serves as a learning example for ML deployment on Azure.

## 📄 **License**

This project is open source and available under the [MIT License](LICENSE).

---

**Built with ❤️ using Azure, Python, and Machine Learning**
