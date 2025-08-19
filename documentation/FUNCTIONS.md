# 🔧 Function Documentation

This document provides detailed technical documentation for all Azure Functions in the Penguin Classifier application.

## 📁 **Function Structure**

```
function_app/
├── ClassifyPenguinSimple/          # Main prediction function
│   ├── __init__.py                 # Function implementation
│   ├── function.json               # Azure Functions binding configuration
│   └── penguins_model.pkl          # Trained ML model (268KB)
├── host.json                       # Global Functions host configuration
└── requirements.txt                # Python dependencies
```

## 🎯 **ClassifyPenguinSimple Function**

### **Purpose**
The primary function that receives penguin measurements and returns species predictions using a cached Random Forest model.

### **HTTP Trigger Configuration**
```json
{
    "scriptFile": "__init__.py",
    "bindings": [
        {
            "authLevel": "anonymous",
            "type": "httpTrigger", 
            "direction": "in",
            "name": "req",
            "methods": ["get", "post", "options"]
        },
        {
            "type": "http",
            "direction": "out", 
            "name": "$return"
        }
    ]
}
```

### **Function Implementation Details**

#### **Model Loading Strategy**
```python
# Global variable to cache the model across function invocations
_model = None

def load_model():
    """Load the model once and cache it for subsequent requests"""
    global _model
    if _model is None:
        # Try multiple paths to locate the model file
        possible_paths = [
            os.path.join(os.path.dirname(__file__), 'penguins_model.pkl'),  # Same directory
            os.path.join(os.path.dirname(__file__), '..', 'models', 'penguins_model.pkl'),  # models folder
            os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'penguins_model.pkl'),  # Original path
        ]
        
        # Load from first available path
        for path in possible_paths:
            if os.path.exists(path):
                _model = joblib.load(path)
                break
```

**Benefits of This Approach:**
- **Performance**: Model loaded once per function instance (cold start)
- **Memory Efficiency**: Shared across warm function invocations  
- **Resilience**: Multiple fallback paths for model location
- **Cost Optimization**: Reduces execution time for subsequent requests

#### **Request Processing Pipeline**

**1. CORS Handling**
```python
# CORS headers for cross-origin requests
headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS", 
    "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Requested-With"
}

# Handle preflight OPTIONS requests
if req.method == "OPTIONS":
    return func.HttpResponse(status_code=204, headers=headers)
```

**2. Input Validation**
```python
# Parse and validate JSON request body
req_body = req.get_json()
features = req_body.get('features', [])

# Ensure exactly 4 numerical features
if not features or len(features) != 4:
    return func.HttpResponse(
        json.dumps({"error": "Features array must contain exactly 4 values"}),
        status_code=400,
        headers=headers,
        mimetype="application/json"
    )
```

**3. ML Prediction**
```python
# Convert to numpy array for scikit-learn
features_array = np.array([features])

# Generate prediction (0, 1, or 2)
prediction = int(model.predict(features_array)[0])

# Calculate confidence scores
probabilities = model.predict_proba(features_array)[0]
confidence = float(max(probabilities))
```

**4. Response Formatting**
```python
# Map numerical prediction to species name
penguin_species = ['Adelie', 'Chinstrap', 'Gentoo']
species_name = penguin_species[prediction]

# Construct comprehensive response
response = {
    "prediction": prediction,           # Numerical class (0, 1, 2)
    "class": species_name,             # Species name
    "species_name": species_name,      # Duplicate for compatibility
    "features": features,              # Echo input features
    "success": True,                   # Success indicator
    "confidence": confidence           # Prediction confidence (0-1)
}
```

### **Input/Output Specifications**

#### **Expected Input**
```json
{
    "features": [39.1, 18.7, 18.1, 37.5]
}
```

**Feature Descriptions:**
- `features[0]`: Culmen Length (mm) - raw measurement
- `features[1]`: Culmen Depth (mm) - raw measurement  
- `features[2]`: Flipper Length - normalized (actual_mm / 10)
- `features[3]`: Body Mass - normalized (actual_grams / 100)

#### **Success Response**
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

#### **Error Response**
```json
{
    "error": "Features array must contain exactly 4 values",
    "success": false,
    "message": "Classification failed"
}
```

### **Performance Characteristics**

- **Cold Start Time**: ~3-5 seconds (model loading)
- **Warm Execution Time**: <100ms
- **Memory Usage**: ~200MB (including model)
- **Throughput**: ~100 requests/second (warm instances)

### **Error Handling**

The function implements comprehensive error handling:

1. **Input Validation Errors**: Invalid JSON, missing features, wrong feature count
2. **Model Loading Errors**: File not found, corrupted model, incompatible versions
3. **Prediction Errors**: Invalid feature values, model inference failures
4. **System Errors**: Memory issues, timeout errors

Each error returns appropriate HTTP status codes and descriptive error messages.

## ⚙️ **Host Configuration**

### **host.json Settings**
```json
{
    "version": "2.0",
    "functionTimeout": "00:05:00",
    "extensions": {
        "http": {
            "routePrefix": "api"
        }
    }
}
```

**Configuration Explanation:**
- **version**: Azure Functions runtime version
- **functionTimeout**: Maximum execution time (5 minutes)
- **routePrefix**: URL prefix for HTTP triggers (/api/)

## 📦 **Dependencies**

### **requirements.txt**
```
azure-functions      # Azure Functions Python bindings
scikit-learn==1.3.2  # Machine learning library
joblib==1.3.2        # Model serialization/loading
numpy==1.24.3        # Numerical computing
```

**Dependency Rationale:**
- **azure-functions**: Required for HTTP triggers and responses
- **scikit-learn**: ML library used to train the Random Forest model
- **joblib**: Efficient loading of serialized scikit-learn models
- **numpy**: Required by scikit-learn for numerical operations

### **Version Compatibility**
- **Python Runtime**: 3.9.7 (Azure Functions v4)
- **scikit-learn**: Fixed version to ensure model compatibility
- **Model File**: Trained with scikit-learn 1.3.2

## 🔄 **Function Lifecycle**

### **Cold Start Process**
1. **Function Instance Creation**: Azure provisions new compute instance
2. **Runtime Initialization**: Python 3.9 environment setup
3. **Dependency Installation**: Load required Python packages
4. **Function Loading**: Import function code and dependencies
5. **Model Loading**: Load and cache ML model (first request only)
6. **Request Processing**: Handle incoming HTTP request

### **Warm Execution Process**
1. **Request Routing**: Azure routes request to warm instance
2. **Model Retrieval**: Use cached model (no loading overhead)
3. **Prediction**: Execute ML inference
4. **Response**: Return JSON result

### **Instance Management**
- **Scaling**: Azure automatically creates instances based on demand
- **Timeout**: Instances hibernate after inactivity (~20 minutes)
- **Memory**: Each instance can handle multiple concurrent requests
- **Statelessness**: No shared state between requests (except cached model)

## 🚀 **Optimization Strategies**

### **Current Optimizations**
1. **Model Caching**: Global variable prevents repeated loading
2. **Minimal Dependencies**: Only essential packages to reduce cold start
3. **Efficient Serialization**: joblib provides fast model loading
4. **Error Handling**: Graceful degradation for various failure modes

### **Future Optimizations**
1. **Model Compression**: Reduce model file size further
2. **Async Processing**: Handle multiple requests concurrently
3. **Response Caching**: Cache predictions for identical inputs
4. **Monitoring**: Add custom telemetry for performance tracking

## 📊 **Monitoring and Observability**

### **Built-in Logging**
```python
import logging

# Function entry/exit logging
logging.info('ClassifyPenguinSimple function processed a request.')

# Model loading success/failure
logging.info(f"Model loaded successfully from {model_path}")
logging.error(f"Error loading model: {str(e)}")
```

### **Application Insights Integration**
- **Request Tracking**: Automatic HTTP request/response logging
- **Performance Metrics**: Execution time, memory usage, throughput
- **Error Tracking**: Exception details and stack traces
- **Custom Events**: Model loading events, prediction metrics

### **Recommended Monitoring**
1. **Response Time**: Track prediction latency trends
2. **Error Rate**: Monitor failed requests and causes
3. **Cold Start Frequency**: Optimize based on usage patterns
4. **Model Performance**: Track prediction confidence distributions

---

This documentation provides the technical foundation for understanding, maintaining, and extending the Penguin Classifier Azure Functions implementation.
