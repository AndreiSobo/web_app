# Copy your trained model to the function app
# This script copies the model file to the function app directory

import shutil
import os

source_model = '/home/andrei/git/web_app/models/penguins_model.pkl'
target_dir = '/home/andrei/git/web_app/function_app/models/'

# Create target directory if it doesn't exist
os.makedirs(target_dir, exist_ok=True)

# Copy model
target_model = os.path.join(target_dir, 'penguins_model.pkl')
shutil.copy2(source_model, target_model)

print(f"Model copied from {source_model} to {target_model}")
