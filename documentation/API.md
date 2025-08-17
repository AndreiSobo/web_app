# 📡 API Documentation

Complete API reference for the Penguin Species Classifier service.

## 🔗 **Base URLs**

- **Production**: `https://penguin-classifier-function.azurewebsites.net`
- **Static Web App**: `https://blue-wave-0b3a88b03.6.azurestaticapps.net`

## 🐧 **Classification Endpoint**

### **POST /api/classifypenguinsimple**

Classifies penguin species based on physical measurements.

#### **Request**

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
    "features": [number, number, number, number]
}
```

**Parameters:**
- `features` (array): Array of exactly 4 numerical values representing:
  - `features[0]`: Culmen Length (mm) - e.g., 39.1
  - `features[1]`: Culmen Depth (mm) - e.g., 18.7
  - `features[2]`: Flipper Length (normalized) - e.g., 18.1 (actual: 181mm)
  - `features[3]`: Body Mass (normalized) - e.g., 37.5 (actual: 3750g)

#### **Response**

**Success Response (200 OK):**
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

**Response Fields:**
- `prediction` (integer): Numerical class prediction (0=Adelie, 1=Chinstrap, 2=Gentoo)
- `class` (string): Species name (legacy field)
- `species_name` (string): Human-readable species name
- `features` (array): Echo of input features
- `success` (boolean): Operation success indicator
- `confidence` (float): Prediction confidence score (0.0-1.0)

**Error Response (400 Bad Request):**
```json
{
    "error": "Features array must contain exactly 4 values",
    "success": false,
    "message": "Classification failed"
}
```

**Error Response (500 Internal Server Error):**
```json
{
    "error": "Model loading failed",
    "success": false,
    "message": "Classification failed"
}
```

#### **Examples**

**Example 1: Adelie Penguin**
```bash
curl -X POST https://penguin-classifier-function.azurewebsites.net/api/classifypenguinsimple \
  -H "Content-Type: application/json" \
  -d '{"features": [39.1, 18.7, 18.1, 37.5]}'
```

**Response:**
```json
{
    "prediction": 0,
    "class": "Adelie", 
    "species_name": "Adelie",
    "features": [39.1, 18.7, 18.1, 37.5],
    "success": true,
    "confidence": 1.0
}
```

**Example 2: Chinstrap Penguin**
```bash
curl -X POST https://penguin-classifier-function.azurewebsites.net/api/classifypenguinsimple \
  -H "Content-Type: application/json" \
  -d '{"features": [44.9, 13.3, 21.3, 51.0]}'
```

**Response:**
```json
{
    "prediction": 1,
    "class": "Chinstrap",
    "species_name": "Chinstrap", 
    "features": [44.9, 13.3, 21.3, 51.0],
    "success": true,
    "confidence": 0.95
}
```

**Example 3: Invalid Input**
```bash
curl -X POST https://penguin-classifier-function.azurewebsites.net/api/classifypenguinsimple \
  -H "Content-Type: application/json" \
  -d '{"features": [39.1, 18.7]}'
```

**Response:**
```json
{
    "error": "Features array must contain exactly 4 values",
    "success": false,
    "message": "Classification failed"
}
```

## 🔍 **Debug Endpoint**

### **GET /api/debugendpoint**

Health check and diagnostic endpoint.

#### **Request**

**Method:** GET  
**Headers:** None required

#### **Response**

**Success Response (200 OK):**
```json
{
    "status": "success",
    "message": "Debug endpoint is working!",
    "available_env_vars": ["FUNCTIONS_WORKER_RUNTIME", "WEBSITE_SITE_NAME", ...],
    "function_app": "found"
}
```

**Response Fields:**
- `status` (string): Health status
- `message` (string): Diagnostic message
- `available_env_vars` (array): List of environment variable names
- `function_app` (string): Function app detection status

#### **Example**

```bash
curl https://penguin-classifier-function.azurewebsites.net/api/debugendpoint
```

## 🔒 **Authentication**

**Current Implementation:** Anonymous access (no authentication required)

**Headers:** No authentication headers needed

**Rate Limiting:** Handled automatically by Azure Functions (throttling under extreme load)

## 📊 **Feature Encoding Guide**

### **Input Feature Transformations**

The model expects normalized inputs for some features:

| Feature | Input Format | Model Format | Transformation |
|---------|--------------|--------------|----------------|
| Culmen Length | 39.1 mm | 39.1 | None (raw value) |
| Culmen Depth | 18.7 mm | 18.7 | None (raw value) |
| Flipper Length | 181 mm | 18.1 | Divide by 10 |
| Body Mass | 3750 g | 37.5 | Divide by 100 |

### **Feature Ranges**

Typical ranges for each species:

| Species | Culmen Length | Culmen Depth | Flipper Length | Body Mass |
|---------|---------------|--------------|----------------|-----------|
| Adelie | 32-46 mm | 15-21 mm | 172-210 mm | 2850-4775 g |
| Chinstrap | 40-58 mm | 16-20 mm | 178-212 mm | 2700-4800 g |
| Gentoo | 40-59 mm | 13-17 mm | 203-231 mm | 3950-6300 g |

## 🎯 **Species Classification**

### **Species Mapping**

| Prediction | Species Name | Scientific Name | Description |
|------------|--------------|-----------------|-------------|
| 0 | Adelie | *Pygoscelis adeliae* | Most widespread Antarctic penguin |
| 1 | Chinstrap | *Pygoscelis antarcticus* | Distinctive black band under head |
| 2 | Gentoo | *Pygoscelis papua* | Largest penguin in the genus |

### **Confidence Interpretation**

- **0.9 - 1.0**: Very high confidence, clear classification
- **0.7 - 0.9**: High confidence, reliable prediction
- **0.5 - 0.7**: Moderate confidence, borderline case
- **< 0.5**: Low confidence, uncertain classification

## 🚦 **HTTP Status Codes**

| Code | Description | Scenario |
|------|-------------|----------|
| 200 | OK | Successful prediction |
| 204 | No Content | OPTIONS preflight request |
| 400 | Bad Request | Invalid input (wrong feature count, invalid JSON) |
| 500 | Internal Server Error | Model loading error, prediction failure |

## 🔄 **CORS Support**

**Allowed Origins:** `*` (all origins)  
**Allowed Methods:** `GET, POST, OPTIONS`  
**Allowed Headers:** `Content-Type, Authorization, X-Requested-With`

**Preflight Requests:** Supported via OPTIONS method

## ⚡ **Performance Specifications**

| Metric | Value | Notes |
|--------|-------|--------|
| Response Time | < 1 second | Warm function instances |
| Cold Start | 3-5 seconds | First request after idle |
| Throughput | ~100 req/sec | Per function instance |
| Timeout | 5 minutes | Maximum execution time |
| Payload Limit | 100 MB | Azure Functions limit |

## 🐛 **Error Handling**

### **Client Errors (4xx)**

**400 Bad Request - Invalid Feature Count:**
```json
{
    "error": "Features array must contain exactly 4 values",
    "success": false,
    "message": "Classification failed"
}
```

**400 Bad Request - Missing Request Body:**
```json
{
    "error": "Request body is required",
    "success": false,
    "message": "Classification failed"
}
```

### **Server Errors (5xx)**

**500 Internal Server Error - Model Loading Failed:**
```json
{
    "error": "Model not found in any of these paths: [...]",
    "success": false,
    "message": "Classification failed"
}
```

**500 Internal Server Error - Prediction Failed:**
```json
{
    "error": "Invalid feature values for prediction",
    "success": false,
    "message": "Classification failed"
}
```

## 📚 **JavaScript SDK Example**

```javascript
class PenguinClassifier {
    constructor(baseUrl = 'https://penguin-classifier-function.azurewebsites.net') {
        this.baseUrl = baseUrl;
    }
    
    async classify(culmenLength, culmenDepth, flipperLength, bodyMass) {
        // Normalize inputs
        const features = [
            culmenLength,
            culmenDepth, 
            flipperLength / 10,  // Normalize flipper length
            bodyMass / 100       // Normalize body mass
        ];
        
        try {
            const response = await fetch(`${this.baseUrl}/api/classifypenguinsimple`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ features })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Classification error:', error);
            throw error;
        }
    }
    
    async health() {
        const response = await fetch(`${this.baseUrl}/api/debugendpoint`);
        return await response.json();
    }
}

// Usage example
const classifier = new PenguinClassifier();

// Classify a penguin
classifier.classify(39.1, 18.7, 181, 3750)
    .then(result => {
        console.log(`Predicted species: ${result.species_name}`);
        console.log(`Confidence: ${(result.confidence * 100).toFixed(1)}%`);
    })
    .catch(error => {
        console.error('Classification failed:', error);
    });
```

## 🔧 **Testing**

### **Automated Testing Script**

```bash
#!/bin/bash
# test_api.sh - Comprehensive API testing

BASE_URL="https://penguin-classifier-function.azurewebsites.net"

echo "Testing Penguin Classifier API..."

# Test 1: Valid Adelie prediction
echo "Test 1: Adelie classification"
curl -s -X POST "$BASE_URL/api/classifypenguinsimple" \
  -H "Content-Type: application/json" \
  -d '{"features": [39.1, 18.7, 18.1, 37.5]}' | jq .

# Test 2: Valid Chinstrap prediction  
echo "Test 2: Chinstrap classification"
curl -s -X POST "$BASE_URL/api/classifypenguinsimple" \
  -H "Content-Type: application/json" \
  -d '{"features": [44.9, 13.3, 21.3, 51.0]}' | jq .

# Test 3: Invalid input (too few features)
echo "Test 3: Invalid input"
curl -s -X POST "$BASE_URL/api/classifypenguinsimple" \
  -H "Content-Type: application/json" \
  -d '{"features": [39.1, 18.7]}' | jq .

# Test 4: Health check
echo "Test 4: Health check"
curl -s "$BASE_URL/api/debugendpoint" | jq .

echo "API testing complete!"
```

---

This API documentation provides complete reference information for integrating with the Penguin Species Classifier service.
