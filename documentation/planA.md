# Plan A+: Architecture Separation Strategy

## 🚨 Current Problem

### The Challenge
Azure Static Web Apps have a **100MB size limit** for API functions. Our penguin classifier application currently uses an integrated architecture where both the frontend and backend functions are deployed together through the Static Web App.

### Current Architecture
```
Azure Static Web App (Integrated)
├── Frontend (HTML/CSS/JS)
├── API Functions
│   ├── ClassifyPenguinSimple function
│   └── XAI function (with SHAP/matplotlib dependencies)
└── Dependencies: shap (~50MB) + matplotlib (~30MB) + other ML libraries
```

### The Problem
- **Package Size**: Heavy ML libraries (shap, matplotlib, scipy, pandas, etc.) push total size beyond 100MB
- **Deployment Failure**: Static Web App rejects deployment with "content too large" error
- **Dependency Conflict**: Can't remove libraries because XAI function requires them for force plots

## 🎯 Plan A+ Solution: Complete Service Separation

### New Architecture
```
Azure Static Web App (Frontend Only)     Azure Functions App (Backend Only)
├── Frontend files only                  ├── ClassifyPenguinSimple function
├── No API functions                     ├── XAI function
├── No heavy dependencies                ├── All ML libraries (shap, matplotlib)
└── Size: <10MB                          └── Size: Can use full 1.5GB limit
    ↓                                        ↑
    HTTP calls across services ──────────────┘
```

### Key Benefits
1. **No Size Limits**: Static Web App has no API = no 100MB constraint
2. **Full ML Capabilities**: Functions App can use heavy libraries without limits
3. **Better Performance**: Functions communicate internally (no HTTP overhead between them)
4. **Cost Optimization**: Static Web App optimized for frontend, Functions App for compute
5. **Independent Scaling**: Each service scales based on its specific needs

## 📋 Implementation Plan

### Phase 1: Prepare Frontend-Only Static Web App
1. **Remove API Functions**: Delete function folders from Static Web App deployment
2. **Update GitHub Actions**: Modify workflow to deploy only frontend files
3. **Clean Dependencies**: Remove all function-related dependencies from root requirements.txt

### Phase 2: Create Dedicated Azure Functions App
1. **Deploy Both Functions**: ClassifyPenguinSimple + XAI to standalone Functions App
2. **Include All Dependencies**: Full ML stack (shap, matplotlib, scipy, pandas, etc.)
3. **Configure CORS**: Allow Static Web App domain to call Functions App

### Phase 3: Update Frontend Configuration
1. **Change API Endpoints**: Point to dedicated Functions App URLs
2. **Handle Cross-Origin**: Configure proper CORS headers and requests
3. **Environment Config**: Different endpoints for dev/staging/production

## 🔧 Technical Implementation

### Deployment Process
```
Frontend Deployment (Automated):
GitHub Actions → Azure Static Web App (frontend files only)

Backend Deployment (Manual):
func azure functionapp publish → Azure Functions App (both functions + ML libraries)
```

### API Communication Flow
```
User Input → Frontend → HTTP Request → Azure Functions App → ClassifyPenguinSimple 
                                                          ↓
                                      Internal Call → XAI Function (with SHAP)
                                                          ↓
Frontend ← JSON Response ← ClassifyPenguinSimple ← Feature Importance Data
```

## 🎯 Expected Outcomes

### Immediate Benefits
- ✅ **Frontend Deploys Successfully**: No size constraints
- ✅ **Backend Handles ML Workloads**: Full access to heavy libraries
- ✅ **XAI Force Plots Work**: SHAP and matplotlib available
- ✅ **Better Performance**: Optimized service separation

### Long-term Advantages
- **Easier Maintenance**: Clear separation of concerns
- **Better Scalability**: Independent service scaling
- **Cost Efficiency**: Right-sized resources for each service
- **Development Flexibility**: Can modify frontend/backend independently

## 🔍 Why This Solves the Problem

The root cause of the deployment failure is the **architectural coupling** of frontend and backend in a single Static Web App deployment. By completely decoupling these services:

1. **Static Web App** serves only static content (no size limits for frontend files)
2. **Azure Functions App** handles compute workloads with appropriate resource limits (1.5GB)
3. **ML Libraries** live where they belong - in the compute service, not the web service

This separation aligns with Azure best practices and provides the optimal architecture for ML-powered web applications.