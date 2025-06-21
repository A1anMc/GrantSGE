from functools import wraps
from typing import Optional, Callable
from flask import request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import redis
import json

# Initialize JWT manager
jwt = JWTManager()

# Initialize Redis for token blacklist
redis_client = redis.Redis(
    host=current_app.config['REDIS_HOST'],
    port=current_app.config['REDIS_PORT'],
    db=current_app.config['REDIS_DB']
)

def init_auth(app):
    """Initialize authentication components."""
    jwt.init_app(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload: dict) -> bool:
        """Check if the token has been revoked."""
        jti = jwt_payload["jti"]
        token_in_redis = redis_client.get(jti)
        return token_in_redis is not None

class RateLimiter:
    """Rate limiting implementation."""
    def __init__(self, key_prefix: str, limit: int, period: int):
        self.key_prefix = key_prefix
        self.limit = limit
        self.period = period

    def is_rate_limited(self, key: str) -> bool:
        """Check if the request is rate limited."""
        redis_key = f"{self.key_prefix}:{key}"
        current = int(datetime.now().timestamp())
        
        try:
            with redis_client.pipeline() as pipe:
                # Clean old records
                pipe.zremrangebyscore(redis_key, 0, current - self.period)
                # Add current request
                pipe.zadd(redis_key, {str(current): current})
                # Count requests in window
                pipe.zcard(redis_key)
                # Set expiry
                pipe.expire(redis_key, self.period)
                
                _, _, count, _ = pipe.execute()
                return count > self.limit
        except redis.RedisError:
            return False

def rate_limit(
    limit: int = 100,
    period: int = 60,
    key_func: Optional[Callable] = None
):
    """Rate limiting decorator."""
    def decorator(f):
        limiter = RateLimiter('rate_limit', limit, period)

        @wraps(f)
        def wrapped(*args, **kwargs):
            key = key_func() if key_func else request.remote_addr
            
            if limiter.is_rate_limited(key):
                return jsonify({
                    'success': False,
                    'error': 'Rate limit exceeded'
                }), 429
            
            return f(*args, **kwargs)
        return wrapped
    return decorator

def role_required(roles):
    """Role-based access control decorator."""
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def wrapped(*args, **kwargs):
            current_user = get_jwt_identity()
            if not any(role in current_user['roles'] for role in roles):
                return jsonify({
                    'success': False,
                    'error': 'Insufficient permissions'
                }), 403
            return f(*args, **kwargs)
        return wrapped
    return decorator

def create_user_token(user_id: int, roles: list) -> str:
    """Create a new access token."""
    expires = timedelta(seconds=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
    identity = {'user_id': user_id, 'roles': roles}
    return create_access_token(identity=identity, expires_delta=expires)

def revoke_token(jti: str, exp: datetime) -> None:
    """Revoke a token by adding it to the blocklist."""
    redis_client.setex(
        jti,
        int((exp - datetime.now()).total_seconds()),
        json.dumps({'revoked': True})
    ) 