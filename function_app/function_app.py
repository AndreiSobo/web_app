import azure.functions as func

# Create the v2 Function App instance
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Register blueprints/endpoints
try:
    from ClassifyPenguinSimple import bp as classify_bp
    app.register_functions(classify_bp)
except Exception as e:
    import logging
    logging.exception("Failed to register ClassifyPenguinSimple blueprint: %s", e)

try:
    from XAI import bp as xai_bp
    app.register_functions(xai_bp)
except Exception as e:
    import logging
    logging.exception("Failed to register XAI blueprint: %s", e)
