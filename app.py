from flask import Flask
from flask_cors import CORS
from api.config import config
from api.auth import init_auth
from api.routes.auth import auth_bp
from api.grants_api import grants_bp
from api.openapi import register_openapi_docs
from api.logging_config import setup_logging
from api.middleware import (
    setup_security_headers,
    setup_request_logging,
    setup_error_handling
)
from api.database import init_db
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
import os

def create_app(config_name='default'):
    """Create Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize Sentry for error tracking
    if os.getenv('SENTRY_DSN'):
        sentry_sdk.init(
            dsn=os.getenv('SENTRY_DSN'),
            integrations=[FlaskIntegration()],
            environment=config_name,
            traces_sample_rate=1.0
        )

    # Setup CORS
    CORS(app, resources={
        r"/api/*": {"origins": app.config['CORS_ORIGINS']}
    })

    # Initialize components
    init_db(app)
    init_auth(app)
    setup_logging(app)
    setup_security_headers(app)
    setup_request_logging(app)
    setup_error_handling(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(grants_bp)

    # Register OpenAPI documentation
    register_openapi_docs(app)

    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200

    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=app.config['DEBUG']
    ) 