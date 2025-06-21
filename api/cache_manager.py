from typing import Any, Dict, Optional, Union
import json
import time
from functools import wraps
import redis
from datetime import datetime, timedelta
import hashlib
import os
import redis
import json
from datetime import timedelta
from typing import Any, Dict, Optional
from functools import wraps
from .monitoring import CACHE_HITS, CACHE_MISSES

class TieredCache:
    """Two-level cache implementation with memory and Redis."""
    
    def __init__(self):
        """Initialize cache with memory and Redis backends."""
        self._memory_cache: Dict[str, Dict[str, Any]] = {}
        self._memory_expiry: Dict[str, datetime] = {}
        self._version = "1.0"
        
        # Initialize Redis connection
        self._redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=int(os.getenv('REDIS_DB', 0)),
            decode_responses=True
        )
    
    def _get_versioned_key(self, key: str) -> str:
        """Get versioned cache key."""
        return f"{self._version}:{key}"
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get value from cache."""
        versioned_key = self._get_versioned_key(key)
        
        # Try memory cache first
        if versioned_key in self._memory_cache:
            if versioned_key not in self._memory_expiry or \
               self._memory_expiry[versioned_key] > datetime.now():
                CACHE_HITS.inc()
                return self._memory_cache[versioned_key]
            else:
                # Expired from memory
                del self._memory_cache[versioned_key]
                if versioned_key in self._memory_expiry:
                    del self._memory_expiry[versioned_key]
        
        # Try Redis
        try:
            redis_value = self._redis_client.get(versioned_key)
            if redis_value:
                value = json.loads(redis_value)
                # Cache in memory
                self._memory_cache[versioned_key] = value
                CACHE_HITS.inc()
                return value
        except (redis.RedisError, json.JSONDecodeError):
            pass
        
        CACHE_MISSES.inc()
        return None
    
    def set(self, key: str, value: Dict[str, Any], memory_ttl: Optional[int] = None) -> None:
        """Set value in cache."""
        versioned_key = self._get_versioned_key(key)
        
        # Set in memory
        self._memory_cache[versioned_key] = value
        if memory_ttl:
            self._memory_expiry[versioned_key] = datetime.now() + timedelta(seconds=memory_ttl)
        
        # Set in Redis
        try:
            self._redis_client.set(versioned_key, json.dumps(value))
        except redis.RedisError:
            pass
    
    def invalidate(self, key: str) -> None:
        """Invalidate cache entry."""
        versioned_key = self._get_versioned_key(key)
        
        # Remove from memory
        if versioned_key in self._memory_cache:
            del self._memory_cache[versioned_key]
        if versioned_key in self._memory_expiry:
            del self._memory_expiry[versioned_key]
        
        # Remove from Redis
        try:
            self._redis_client.delete(versioned_key)
        except redis.RedisError:
            pass
    
    def invalidate_pattern(self, pattern: str) -> None:
        """Invalidate all keys matching pattern."""
        versioned_pattern = self._get_versioned_key(pattern)
        
        # Remove from memory
        memory_keys = [k for k in self._memory_cache.keys() if k.startswith(versioned_pattern)]
        for k in memory_keys:
            del self._memory_cache[k]
            if k in self._memory_expiry:
                del self._memory_expiry[k]
        
        # Remove from Redis
        try:
            redis_keys = self._redis_client.scan_iter(match=versioned_pattern)
            for k in redis_keys:
                self._redis_client.delete(k)
        except redis.RedisError:
            pass
    
    def update_version(self, new_version: str) -> None:
        """Update cache version to invalidate all entries."""
        self._version = new_version
        self._memory_cache.clear()
        self._memory_expiry.clear()
    
    def clear_all(self) -> None:
        """Clear all cache entries."""
        self._memory_cache.clear()
        self._memory_expiry.clear()
        try:
            self._redis_client.flushdb()
        except redis.RedisError:
            pass

def cached(key_prefix: str):
    """Decorator for caching function results."""
    cache = TieredCache()
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            key_parts = [key_prefix]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
            cache_key = ":".join(key_parts)
            
            # Try to get from cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Call function and cache result
            result = await func(*args, **kwargs)
            cache.set(cache_key, result)
            return result
        
        return wrapper
    return decorator

# Global cache instance
cache = TieredCache() 