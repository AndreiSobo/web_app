Instructions to run the app

## Docker Commands

- `docker-compose build` - Build the container images
- `docker-compose up` - Build (if needed) and start the containers
- `docker-compose up -d` - Build (if needed) and start the containers in detached mode (background)
- `docker-compose up -d --build` - Force rebuild and start the containers in detached mode
- `docker-compose ps` - Check status once its running
- `docker-compose down` - Stop and remove containers

## Curl command for predictions

curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [38.2, 18.1, 18.5, 38]}'

[44.9, 13.3, 21.3, 51.0]

curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [44.9, 13.3, 21.3, 51.0] }'


## Project requirements and Dockerfile

# Flask Application Requirements (requirements.txt)
flask==2.3.3
requests==2.31.0
werkzeug==2.3.7
python-dotenv==1.0.0

# Azure Function Requirements (requirements.txt for function)
azure-functions==1.15.0
azure-identity==1.13.0
azure-mgmt-containerinstance==10.1.0
requests==2.31.0

# Container Requirements (requirements.txt for container)
torch==2.0.1
torchvision==0.15.2
Pillow==10.0.0
numpy==1.24.3

# Dockerfile for Container Image
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your model and code
COPY container_app.py .
COPY models/ ./models/

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run when container starts
CMD ["python", "container_app.py"]