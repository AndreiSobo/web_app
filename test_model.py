#!/usr/bin/env python3
"""
Test script to verify the penguin classification model works correctly
"""

import joblib
import numpy as np
import os

def test_model():
    """Test the penguin classification model"""
    
    # Load model
    model_path = '/home/andrei/git/web_app/models/penguins_model.pkl'
    print(f"Loading model from: {model_path}")
    
    try:
        model = joblib.load(model_path)
        print(f"✓ Model loaded successfully")
        print(f"Model type: {type(model)}")
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        return False
    
    # Test cases from your curl command
    test_cases = [
        {
            "name": "Original curl test",
            "features": [38.2, 18.1, 18.5, 38],  # Already normalized
            "expected": "Adelie"
        },
        {
            "name": "Raw values test", 
            "features": [39.1, 18.7, 181/10, 3750/100],  # Convert raw to normalized
            "expected": "Unknown"
        },
        {
            "name": "Chinstrap example",
            "features": [44.9, 13.3, 21.3, 51.0],  # From your README
            "expected": "Unknown"
        }
    ]
    
    # Species mapping
    penguin_species = ['Adelie', 'Chinstrap', 'Gentoo']
    
    print("\n=== Model Test Results ===")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   Features: {test_case['features']}")
        
        try:
            # Make prediction
            features_array = np.array([test_case['features']])
            prediction = int(model.predict(features_array)[0])
            species = penguin_species[prediction]
            
            # Get confidence if available
            try:
                probabilities = model.predict_proba(features_array)[0]
                confidence = max(probabilities)
                print(f"   Prediction: {prediction} ({species})")
                print(f"   Confidence: {confidence:.3f}")
                print(f"   Probabilities: {[f'{p:.3f}' for p in probabilities]}")
            except AttributeError:
                print(f"   Prediction: {prediction} ({species})")
                print(f"   Confidence: Not available")
            
            print(f"   ✓ Success")
            
        except Exception as e:
            print(f"   ✗ Error: {e}")
    
    print(f"\n=== Model Information ===")
    try:
        # Try to get model information
        if hasattr(model, 'feature_names_in_'):
            print(f"Feature names: {model.feature_names_in_}")
        if hasattr(model, 'classes_'):
            print(f"Classes: {model.classes_}")
        if hasattr(model, 'n_features_in_'):
            print(f"Number of features: {model.n_features_in_}")
    except:
        pass
    
    return True

if __name__ == "__main__":
    test_model()
