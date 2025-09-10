import azure.functions as func

# Create the v2 Function App instance
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Register blueprints/endpoints
try:
    from .ClassifyPenguinSimple import bp as classify_bp
    app.register_functions(classify_bp)
except Exception as e:
    # Fallback: log import errors at startup; Functions host will show this.
    import logging
    logging.exception("Failed to register ClassifyPenguinSimple blueprint: %s", e)
