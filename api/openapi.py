from flask import Blueprint, jsonify, send_from_directory
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields

# Create APISpec
spec = APISpec(
    title="Grant Application Dashboard API",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

# Schemas
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    roles = fields.List(fields.Str())
    is_active = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    last_login = fields.DateTime(dump_only=True)

class GrantSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    funder = fields.Str(required=True)
    source_url = fields.Str()
    due_date = fields.DateTime()
    amount_string = fields.Str()
    description = fields.Str()
    status = fields.Str()
    eligibility_analysis = fields.Dict()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

# Register schemas
spec.components.schema("User", schema=UserSchema)
spec.components.schema("Grant", schema=GrantSchema)

# Security schemes
spec.components.security_scheme(
    "bearerAuth",
    {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    },
)

# Add basic info
spec.tag({"name": "auth", "description": "Authentication operations"})
spec.tag({"name": "grants", "description": "Grant management operations"})

def register_openapi_docs(app):
    """Register OpenAPI documentation routes."""
    
    docs_bp = Blueprint('docs', __name__)

    @docs_bp.route('/api/docs/openapi.json')
    def get_openapi_spec():
        """Get OpenAPI specification."""
        return jsonify(spec.to_dict())

    @docs_bp.route('/api/docs')
    def get_docs():
        """Serve Swagger UI."""
        return send_from_directory('static', 'swagger-ui.html')

    # Document auth endpoints
    with app.test_request_context():
        spec.path(
            path="/api/auth/register",
            operations={
                "post": {
                    "tags": ["auth"],
                    "summary": "Register a new user",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": UserSchema
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "User created successfully",
                            "content": {
                                "application/json": {
                                    "schema": UserSchema
                                }
                            }
                        }
                    }
                }
            }
        )

        spec.path(
            path="/api/auth/login",
            operations={
                "post": {
                    "tags": ["auth"],
                    "summary": "Login user",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "email": {"type": "string"},
                                        "password": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Login successful",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "token": {"type": "string"},
                                            "user": {"$ref": "#/components/schemas/User"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        )

    # Document grant endpoints
    with app.test_request_context():
        spec.path(
            path="/api/grants",
            operations={
                "get": {
                    "tags": ["grants"],
                    "summary": "Get all grants",
                    "security": [{"bearerAuth": []}],
                    "parameters": [
                        {
                            "name": "status",
                            "in": "query",
                            "schema": {"type": "string"}
                        },
                        {
                            "name": "funder",
                            "in": "query",
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "List of grants",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Grant"}
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "tags": ["grants"],
                    "summary": "Create a new grant",
                    "security": [{"bearerAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": GrantSchema
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "Grant created successfully",
                            "content": {
                                "application/json": {
                                    "schema": GrantSchema
                                }
                            }
                        }
                    }
                }
            }
        )

    app.register_blueprint(docs_bp) 