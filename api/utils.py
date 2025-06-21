import time
from functools import wraps
from typing import Any, Callable, Dict, Optional
import redis
import json
from datetime import timedelta
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Initialize Redis client for rate limiting and caching
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=0,
    decode_responses=True
)

def get_db_session() -> Session:
    """Create a database session."""
    engine = create_engine(os.getenv('DATABASE_URL', 'sqlite:///grants.db'))
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

class Cache:
    """Simple cache implementation."""
    _instance = None
    _redis_client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._redis_client = redis.Redis(
                host=os.getenv('REDIS_HOST', 'localhost'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                db=int(os.getenv('REDIS_DB', 0)),
                decode_responses=True
            )
        return cls._instance

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            value = self._redis_client.get(key)
            return value
        except redis.RedisError:
            return None

    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """Set value in cache with TTL."""
        try:
            self._redis_client.setex(key, ttl, value)
        except redis.RedisError:
            pass

class RateLimiter:
    """Simple rate limiter implementation."""
    _instance = None
    _redis_client = None
    _window = 60  # 1 minute window
    _max_requests = 10  # Maximum requests per window

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._redis_client = redis.Redis(
                host=os.getenv('REDIS_HOST', 'localhost'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                db=int(os.getenv('REDIS_DB', 0)),
                decode_responses=True
            )
        return cls._instance

    def is_rate_limited(self, key: str) -> bool:
        """Check if rate limit is exceeded."""
        try:
            current = int(time.time())
            window_key = f"{key}:{current // self._window}"
            
            count = self._redis_client.get(window_key)
            if count is None:
                self._redis_client.setex(window_key, self._window, 1)
                return False
            
            count = int(count)
            if count >= self._max_requests:
                return True
            
            self._redis_client.incr(window_key)
            return False
        except redis.RedisError:
            return False  # Fail open if Redis is down

def rate_limit(limit: int = 10, period: int = 3600):
    """
    Rate limiting decorator.
    
    Args:
        limit: Number of allowed requests per period
        period: Time period in seconds
    """
    def decorator(func: Callable):
        limiter = RateLimiter()
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Use grant_id as the rate limit key
            grant_id = kwargs.get('grant_id') or args[0]
            if limiter.is_rate_limited(str(grant_id)):
                raise Exception("Rate limit exceeded. Please try again later.")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def cache_result(expire_in: int = 3600):
    """
    Cache decorator.
    
    Args:
        expire_in: Cache expiration time in seconds
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Use grant_id as cache key
            grant_id = kwargs.get('grant_id') or args[0]
            cache_key = f"eligibility_scan:{grant_id}"
            
            # Try to get from cache
            cached_result = Cache().get(cache_key)
            if cached_result:
                return cached_result
            
            # Get fresh result
            result = await func(*args, **kwargs)
            
            # Cache the result
            Cache().set(cache_key, result, expire_in)
            return result
        return wrapper
    return decorator 