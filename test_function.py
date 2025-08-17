#!/usr/bin/env python3
"""
Test the new ClassifyPenguinSimple function locally
"""

import sys
import os
sys.path.append('/home/andrei/git/web_app/function_app')

# Mock the Azure Functions context
class MockHttpRequest:
    def __init__(self, method="POST", body=None):
        self.method = method
        self._body = body
    
    def get_json(self):
        import json
        return json.loads(self._body) if self._body else {}

class MockHttpResponse:
    def __init__(self, body, status_code=200, headers=None, mimetype=None):
        self.body = body
        self.status_code = status_code
        self.headers = headers or {}
        self.mimetype = mimetype

# Mock azure.functions
class MockFunctions:
    class HttpRequest(MockHttpRequest):
        pass
    
    class HttpResponse(MockHttpResponse):
        pass

# Replace azure.functions with our mock
sys.modules['azure.functions'] = MockFunctions()

# Now import our function
from ClassifyPenguinSimple import main

def test_function():
    """Test the ClassifyPenguinSimple function"""
    
    print("Testing ClassifyPenguinSimple function...")
    
    # Test case 1: Valid input
    test_request = MockHttpRequest(
        method="POST",
        body='{"features": [39.1, 18.7, 18.1, 37.5]}'
    )
    
    try:
        response = main(test_request)
        print(f"✓ Status Code: {response.status_code}")
        print(f"✓ Response Body: {response.body}")
        print(f"✓ Headers: {response.headers}")
        
        # Parse response
        import json
        result = json.loads(response.body)
        
        if result.get('success'):
            print(f"✅ Prediction: {result.get('species_name')} (confidence: {result.get('confidence', 'N/A')})")
        else:
            print(f"❌ Function returned error: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Error testing function: {e}")
        import traceback
        traceback.print_exc()
    
    # Test case 2: Invalid input
    print("\n--- Testing invalid input ---")
    test_request_invalid = MockHttpRequest(
        method="POST", 
        body='{"features": [1, 2, 3]}'  # Only 3 features instead of 4
    )
    
    try:
        response = main(test_request_invalid)
        print(f"✓ Status Code: {response.status_code}")
        result = json.loads(response.body)
        print(f"✓ Error handling: {result.get('error')}")
    except Exception as e:
        print(f"❌ Error testing invalid input: {e}")

if __name__ == "__main__":
    test_function()
