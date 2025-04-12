# container_app.py
# This code would run in your Azure Container Instance

import os
import sys
import json
import base64
import numpy as np
from PIL import Image
import io
import torch
import torchvision.transforms as transforms

# Load pre-trained model (example with PyTorch)
def load_model():
    # Replace this with your actual model loading code
    try:
        # Example: load a pre-trained ResNet model
        model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet50', pretrained=True)
        model.eval()
        return model
    except Exception as e:
        sys.stderr.write(f"Error loading model: {str(e)}\n")
        sys.exit(1)

# Process image with the model
def process_image(image_data, parameter_value):
    try:
        # Decode base64 image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Apply any preprocessing based on the parameter
        # This is just an example - adjust according to your model's needs
        brightness_factor = 1.0 + (parameter_value / 10.0)
        
        # Apply some preprocessing (example: adjust brightness)
        enhancer = transforms.ColorJitter(brightness=brightness_factor)
        processed_image = enhancer(image)
        
        # Prepare for model input
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        
        input_tensor = preprocess(processed_image)
        input_batch = input_tensor.unsqueeze(0)
        
        # Move to GPU if available
        if torch.cuda.is_available():
            input_batch = input_batch.to('cuda')
            model.to('cuda')
        
        # Get model prediction
        with torch.no_grad():
            output = model(input_batch)
        
        # Process the output (example: get top prediction)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        confidence = probabilities.max().item()
        
        # Convert processed image back to base64 for return
        buffered = io.BytesIO()
        processed_image.save(buffered, format="JPEG")
        processed_image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # Return results
        return {
            "processedImage": processed_image_base64,
            "outputMetrics": f"Confidence: {confidence:.4f}"
        }
        
    except Exception as e:
        sys.stderr.write(f"Error processing image: {str(e)}\n")
        return {
            "error": str(e)
        }

def main():
    try:
        # Get input from environment variables
        image_base64 = os.environ.get("IMAGE_BASE64")
        parameters_str = os.environ.get("PARAMETERS", "0")
        
        # Convert parameters to float
        parameters = float(parameters_str)
        
        # Load the model
        model = load_model()
        
        # Process the image
        result = process_image(image_base64, parameters)
        
        # Output results as JSON to stdout (will be captured in container logs)
        print(json.dumps(result))
        
    except Exception as e:
        sys.stderr.write(f"Container error: {str(e)}\n")
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()