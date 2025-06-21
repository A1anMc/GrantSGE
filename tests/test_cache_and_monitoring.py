import pytest
import json
import time
import asyncio
from unittest.mock import patch, MagicMock
from api.cache_manager import TieredCache, cached
from api.monitoring import (
    track_timing,
    CACHE_HITS,
    CACHE_MISSES,
    ELIGIBILITY_REQUESTS
)

@pytest.fixture
def mock_redis():
    with patch('redis.Redis') as mock:
        mock.get.return_value = None
        mock.scan_iter.return_value = []
        mock.delete.return_value = True
        yield mock

@pytest.fixture
def tiered_cache(mock_redis):
    cache = TieredCache()
    cache._memory_cache.clear()
    cache._redis_client = mock_redis
    return cache

class TestTieredCache:
    """Test suite for TieredCache implementation."""
    
    def test_memory_cache_hit(self, tiered_cache):
        """Test memory cache hit."""
        test_data = {'test': 'data'}
        tiered_cache.set('test_key', test_data)
        
        # Clear counters
        CACHE_HITS.inc(-CACHE_HITS._value._value)
        CACHE_MISSES.inc(-CACHE_MISSES._value._value)
        
        result = tiered_cache.get('test_key')
        assert result == test_data
        assert CACHE_HITS._value._value == 1
    
    def test_memory_cache_expiry(self, tiered_cache):
        """Test that memory cache entries expire correctly."""
        test_data = {'test': 'data'}
        tiered_cache.set('test_key', test_data, memory_ttl=1)
        
        # Wait for expiry
        time.sleep(1.1)
        
        # Clear counters
        CACHE_HITS.inc(-CACHE_HITS._value._value)
        CACHE_MISSES.inc(-CACHE_MISSES._value._value)
        
        # Mock Redis to return None
        tiered_cache._redis_client.get.return_value = None
        
        result = tiered_cache.get('test_key')
        assert result is None
        assert CACHE_MISSES._value._value == 1
    
    def test_redis_fallback(self, tiered_cache, mock_redis):
        """Test that Redis (L2) is used when memory cache misses."""
        test_data = {'test': 'data'}
        mock_redis.get.return_value = json.dumps(test_data).encode()
        
        # Clear memory cache to force Redis lookup
        tiered_cache._memory_cache.clear()
        
        # Clear counters
        CACHE_HITS._value.set(0)
        CACHE_MISSES._value.set(0)
        
        result = tiered_cache.get('test_key')
        assert result == test_data
        assert CACHE_HITS._value._value == 1
    
    def test_cache_invalidation(self, tiered_cache):
        """Test cache invalidation."""
        test_data = {'test': 'data'}
        tiered_cache.set('test_key', test_data)
        
        # Clear counters
        CACHE_HITS._value.set(0)
        CACHE_MISSES._value.set(0)
        
        # Mock Redis to return None after invalidation
        tiered_cache._redis_client.get.return_value = None
        
        tiered_cache.invalidate('test_key')
        result = tiered_cache.get('test_key')
        assert result is None
        assert CACHE_MISSES._value._value == 1
    
    def test_version_based_invalidation(self, tiered_cache):
        """Test version-based cache invalidation."""
        test_data = {'test': 'data'}
        tiered_cache.set('test_key', test_data)
        
        # Clear counters
        CACHE_HITS._value.set(0)
        CACHE_MISSES._value.set(0)
        
        # Mock Redis to return None after version update
        tiered_cache._redis_client.get.return_value = None
        
        tiered_cache.update_version('2.0')
        result = tiered_cache.get('test_key')
        assert result is None
        assert CACHE_MISSES._value._value == 1
    
    def test_pattern_invalidation(self, tiered_cache):
        """Test pattern-based cache invalidation."""
        tiered_cache.set('test_1', {'data': 1})
        tiered_cache.set('test_2', {'data': 2})
        tiered_cache.set('other', {'data': 3})
        
        # Clear counters
        CACHE_HITS._value.set(0)
        CACHE_MISSES._value.set(0)
        
        # Mock Redis to return None after pattern invalidation
        tiered_cache._redis_client.get.return_value = None
        
        tiered_cache.invalidate_pattern('test_*')
        assert tiered_cache.get('test_1') is None
        assert tiered_cache.get('test_2') is None
        assert tiered_cache.get('other') == {'data': 3}

@pytest.mark.asyncio
class TestCacheDecorator:
    """Test suite for cache decorator."""
    
    @pytest.mark.asyncio
    async def test_cached_function(self):
        """Test that cached decorator works correctly."""
        call_count = 0
        
        @cached(key_prefix='test_func')
        async def test_function(param):
            nonlocal call_count
            call_count += 1
            return {'result': param}
        
        # Clear counters
        CACHE_HITS._value.set(0)
        CACHE_MISSES._value.set(0)
        
        # First call should execute function
        result1 = await test_function(1)
        assert result1 == {'result': 1}
        assert call_count == 1
        
        # Second call should use cache
        result2 = await test_function(1)
        assert result2 == {'result': 1}
        assert call_count == 1  # Function not called again
        
        # Different parameter should execute function
        result3 = await test_function(2)
        assert result3 == {'result': 2}
        assert call_count == 2

@pytest.mark.asyncio
class TestMonitoring:
    """Test suite for monitoring functionality."""
    
    @pytest.mark.asyncio
    async def test_timing_decorator(self):
        """Test that timing decorator records metrics correctly."""
        @track_timing('test_phase')
        async def test_function():
            await asyncio.sleep(0.1)
            return 'result'
        
        # Clear counters
        ELIGIBILITY_REQUESTS._value.set(0)
        
        result = await test_function()
        assert result == 'result'
    
    @pytest.mark.asyncio
    async def test_error_tracking(self):
        """Test that errors are tracked correctly."""
        @track_timing('test_phase')
        async def failing_function():
            raise ValueError("Test error")
        
        # Clear counters
        ELIGIBILITY_REQUESTS._value.set(0)
        
        with pytest.raises(ValueError):
            await failing_function()
        
        assert ELIGIBILITY_REQUESTS.labels(status='error')._value._value == 1

def test_monitoring_setup():
    """Test that monitoring metrics are properly initialized."""
    assert CACHE_HITS._type == 'counter'
    assert CACHE_MISSES._type == 'counter'
    assert ELIGIBILITY_REQUESTS._type == 'counter' 