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
curl -X POST https://blue-wave-0b3a88b03.6.azurestaticapps.net/api/classifypenguinsimple \
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

### **System Overview**
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────┐
│   Web Browser   │ ── │ Azure Function   │ ── │ Prediction  │
│  (Static App)   │    │ (Python 3.10)    │    │  Response   │
└─────────────────┘    └──────────────────┘    └─────────────┘
```

**Components:**
1. **Frontend**: Azure Static Web App (HTML/CSS/JavaScript)
2. **Backend**: Azure Functions (Python + ML Model)
3. **Model**: Random Forest Classifier (scikit-learn)

**Why This Architecture:**
- **Cost Effective**: ~$0.001 per prediction vs traditional servers
- **Fast Response**: <1 second prediction time
- **Auto-Scaling**: Handles traffic spikes automatically
- **Serverless**: No infrastructure management required

## 📊 **Machine Learning Model**

- **Algorithm**: Random Forest Classifier
- **Accuracy**: >97% on test dataset
- **Input**: 4 penguin measurements (culmen, flipper, body mass)
- **Output**: Species classification (Adelie, Chinstrap, or Gentoo) with confidence score
- **Training Data**: Palmer Penguins dataset from Antarctica research stations

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
├── static/                    # Frontend web application
├── function_app/              # Azure Functions backend
├── models/                    # ML model files
├── notebooks/                 # Data science workflows
├── data/                      # Training data
└── documentation/             # Technical documentation
```

## 🧪 **Quick Testing**

### **Web Interface Testing**
1. Visit: https://blue-wave-0b3a88b03.6.azurestaticapps.net/
2. Enter penguin measurements or use the "Use Values" buttons
3. Click "Classify Penguin Species" to see prediction results

### **API Testing**
```bash
curl -X POST https://blue-wave-0b3a88b03.6.azurestaticapps.net/api/classifypenguinsimple \
  -H "Content-Type: application/json" \
  -d '{"features": [39.1, 18.7, 18.1, 37.5]}'
```

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

# Local development
cd function_app && func host start    # Start Azure Functions locally
cd static && python -m http.server   # Serve static files
```

### **Deployment**
- **Automatic**: Push to GitHub triggers auto-deployment via GitHub Actions
- **Manual**: Deploy via Azure CLI or VS Code Azure extensions

For detailed technical implementation, see **[Technical Documentation](documentation/TECHNICAL_OVERVIEW.md)**

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
