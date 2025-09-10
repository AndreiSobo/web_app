import logging
import joblib
import os
import azure.functions as func
import matplotlib
import shap

# must take the model output, the model object and the background object and create an explainer object
# with the explainer object create local explanations and also the plot 
# once that is done, wrap it all in a package and send it to the webapp via http. Check if the image should be sent differently. 
# TODO make sure the image is sent, as the deblurring project will need a function (maybe within a container) to send images back to the user.
_model = None
_background = None

def load_model():
    if _model is None:
        try:
            model_path = os.path.join(os.path.dirname(__file__), 'penguins_model.pkl')
        except Exception as e:
            print(f"problems with model_path: {str(e)}")
    try:
        _model = joblib.load(model_path)
        return _model
    except Exception as e:
        print(f"model was not loaded: {str(e)}")

def load_background():
    if _background is None:
        try:
            background_path = os.path.join(os.path.dirname(__file__), 'background_object.pkl')
        except Exception as e:
            print(f"background path error: {str(e)}")
    try:
        _background = joblib.load(background_path)
        return _background
    except Exception as e:
        print(f"could not load background object: {str(e)}")
    
    



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('second function generating XAI')

    # CORS headers
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Requested-With"
    }
    
    # Handle OPTIONS request for CORS preflight
    if req.method == "OPTIONS":
        return func.HttpResponse(status_code=204, headers=headers)

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
