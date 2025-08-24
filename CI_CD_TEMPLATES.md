# 🚀 Standardized CI/CD Templates

## Azure Static Web Apps Template

```yaml
name: Azure Static Web Apps CI/CD

on:
  push:
    branches: [ main, develop ]  # Use 'main' as modern default
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches: [ main ]

env:
  APP_LOCATION: "./static"           # Configurable app location
  API_LOCATION: "./function_app"     # Configurable API location
  OUTPUT_LOCATION: ""                # Build output directory

jobs:
  build_and_deploy_job:
    if: github.event_name == 'push' || (github.event_name == 'pull_request' && github.event.action != 'closed')
    runs-on: ubuntu-latest
    name: Build and Deploy Job
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4        # Latest version
        with:
          submodules: true
          lfs: false
      
      - name: Setup Node.js (if needed)
        uses: actions/setup-node@v4
        with:
          node-version: '18'
        if: needs.setup.outputs.frontend == 'node'
      
      - name: Setup Python (if needed)
        uses: actions/setup-python@v5
        with:
          python-version: '3.9'
        if: needs.setup.outputs.api == 'python'
      
      - name: Build And Deploy
        id: builddeploy
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: "upload"
          app_location: ${{ env.APP_LOCATION }}
          api_location: ${{ env.API_LOCATION }}
          output_location: ${{ env.OUTPUT_LOCATION }}

  close_pull_request_job:
    if: github.event_name == 'pull_request' && github.event.action == 'closed'
    runs-on: ubuntu-latest
    name: Close Pull Request Job
    steps:
      - name: Close Pull Request
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          action: "close"
```

## Azure Functions Template

```yaml
name: Build and Deploy Azure Functions

on:
  push:
    branches: [ main ]
    paths: [ 'function_app/**' ]  # Only trigger on function changes
  workflow_dispatch:             # Manual trigger option

# 🚀 **RECOMMENDATION: Your Current YAMLs are PERFECT!**

## **Analysis: Why CI_CD_TEMPLATES.md is UNNECESSARY**

Your existing workflows are **well-designed and sufficient**. The templates below are for **future projects** or **advanced scenarios only**.

### **Your Current Setup is Ideal Because:**
- ✅ **Simple and working** - no over-engineering
- ✅ **Azure handles Python runtime** automatically  
- ✅ **Minimal complexity** - easier to maintain
- ✅ **Fast deployments** - no unnecessary steps

---

## **Simplified Templates (For Future Reference Only)**

### **Azure Static Web Apps Template** 
*(Based on your working version)*

```yaml
name: Azure Static Web Apps CI/CD

on:
  push:
    branches: [ master ]  # Keep your current branch name
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches: [ master ]

jobs:
  build_and_deploy_job:
    if: github.event_name == 'push' || (github.event_name == 'pull_request' && github.event.action != 'closed')
    runs-on: ubuntu-latest
    name: Build and Deploy Job
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4        # Updated version only
        with:
          submodules: true
          lfs: false
      
      - name: Build And Deploy
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: "upload"
          app_location: "./static"
          api_location: "./function_app"
          output_location: ""

  close_pull_request_job:
    if: github.event_name == 'pull_request' && github.event.action == 'closed'
    runs-on: ubuntu-latest
    name: Close Pull Request Job
    steps:
      - name: Close Pull Request
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          action: "close"
```

### **Azure Functions Template**
*(Based on your working version)*

```yaml
name: Build and Deploy Azure Functions

on:
  push:
    branches: [ master ]
  workflow_dispatch:

env:
  AZURE_FUNCTIONAPP_PACKAGE_PATH: '.'
  PYTHON_VERSION: '3.9'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python  # Only needed for explicit Function App deployment
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Create virtual environment
        run: |
          python -m venv venv
          source venv/bin/activate

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Create deployment package
        run: zip release.zip ./* -r

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: python-app
          path: release.zip

  deploy:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Download artifact
        uses: actions/download-artifact@v4
        with:
          name: python-app

      - name: Unzip for deployment
        run: unzip release.zip

      - name: Deploy to Azure Functions
        uses: Azure/functions-action@v1
        with:
          app-name: 'penguin-classifier-function'
          slot-name: 'Production'
          package: ${{ env.AZURE_FUNCTIONAPP_PACKAGE_PATH }}
          publish-profile: ${{ secrets.AZUREAPPSERVICE_PUBLISHPROFILE }}
```

---

## **CONCLUSION: Keep Your Current YAMLs!**

Your existing workflows are **production-ready and optimal**. The templates above are only useful for:
- 📚 Learning purposes
- 🔄 Future projects with different requirements  
- 📈 When you need to add testing or more complex builds

**No changes needed to your current setup!** 🎯
```
