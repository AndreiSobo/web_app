import logging

import azure.functions as func

# must take the model output, the model object and the background object and create an explainer object
# with the explainer object create local explanations and also the plot 
# once that is done, wrap it all in a package and send it to the webapp via http. Check if the image should be sent differently. 
# TODO make sure the image is sent, as the deblurring project will need a function (maybe within a container) to send images back to the user.

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

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
