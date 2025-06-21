from functools import wraps
from flask import request, jsonify, current_app
import re
import bleach
from typing import Dict, Any, Callable
import logging

logger = logging.getLogger(__name__)

def sanitize_input(data: Any) -> Any:
    """Sanitize input data."""
    if isinstance(data, str):
        return bleach.clean(data)
    elif isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(item) for item in data]
    return data

def validate_json_payload(schema: Dict[str, Any]) -> Callable:
    """Validate JSON payload against schema."""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({
                    'success': False,
                    'error': 'Content-Type must be application/json'
                }), 400

            data = request.get_json()
            
            # Validate required fields
            for field, field_schema in schema.items():
                if field_schema.get('required', False):
                    if field not in data:
                        return jsonify({
                            'success': False,
                            'error': f'Missing required field: {field}'
                        }), 400

                    if field in data and field_schema.get('type'):
                        if not isinstance(data[field], field_schema['type']):
                            return jsonify({
                                'success': False,
                                'error': f'Invalid type for field {field}'
                            }), 400

                # Validate pattern if specified
                if 'pattern' in field_schema and field in data:
                    pattern = re.compile(field_schema['pattern'])
                    if not pattern.match(str(data[field])):
                        return jsonify({
                            'success': False,
                            'error': f'Invalid format for field {field}'
                        }), 400

            # Sanitize input
            request._cached_json = sanitize_input(data)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def setup_security_headers(app):
    """Configure security headers."""
    @app.after_request
    def add_security_headers(response):
        """Add security headers to response."""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        return response

def setup_request_logging(app):
    """Configure request logging."""
    @app.before_request
    def log_request_info():
        """Log request information."""
        logger.info(
            'Request',
            extra={
                'method': request.method,
                'path': request.path,
                'remote_addr': request.remote_addr,
                'user_agent': request.user_agent.string
            }
        )

    @app.after_request
    def log_response_info(response):
        """Log response information."""
        logger.info(
            'Response',
            extra={
                'status': response.status_code,
                'content_length': response.content_length
            }
        )
        return response

def setup_error_handling(app):
    """Configure error handling."""
    @app.errorhandler(400)
    def bad_request(error):
        """Handle bad request errors."""
        return jsonify({
            'success': False,
            'error': 'Bad request',
            'message': str(error)
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        """Handle unauthorized errors."""
        return jsonify({
            'success': False,
            'error': 'Unauthorized',
            'message': str(error)
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        """Handle forbidden errors."""
        return jsonify({
            'success': False,
            'error': 'Forbidden',
            'message': str(error)
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        """Handle not found errors."""
        return jsonify({
            'success': False,
            'error': 'Not found',
            'message': str(error)
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle internal server errors."""
        logger.error(f'Internal Server Error: {error}', exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500 