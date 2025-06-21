from prometheus_client import Counter, Histogram, Gauge, Info
import time
from functools import wraps
from typing import Callable
import psutil
import asyncio

# Prometheus metrics
ELIGIBILITY_REQUESTS = Counter(
    'grant_eligibility_requests',
    'Number of eligibility scan requests',
    ['status']
)

ELIGIBILITY_LATENCY = Histogram(
    'grant_eligibility_latency_seconds',
    'Time taken for eligibility scans',
    ['phase']
)

CACHE_HITS = Counter(
    'grant_eligibility_cache_hits',
    'Number of cache hits'
)

CACHE_MISSES = Counter(
    'grant_eligibility_cache_misses',
    'Number of cache misses'
)

API_RATE_LIMITS = Counter(
    'grant_eligibility_rate_limits_total',
    'Number of rate limit hits'
)

SYSTEM_MEMORY = Gauge(
    'grant_system_memory_bytes',
    'Current system memory usage'
)

CPU_USAGE = Gauge(
    'grant_cpu_usage_percent',
    'Current CPU usage percentage'
)

AI_MODEL_INFO = Info(
    'grant_ai_model',
    'Information about the AI model being used'
)

# Draft generation metrics
DRAFT_REQUESTS = Counter(
    'grant_draft_requests_total',
    'Total number of draft generation requests',
    ['status']  # success, error
)

DRAFT_LATENCY = Histogram(
    'grant_draft_duration_seconds',
    'Time spent generating draft responses',
    ['phase']  # api_call, total
)

def track_timing(phase: str):
    """Decorator to track timing of function execution."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                ELIGIBILITY_LATENCY.labels(phase=phase).observe(time.time() - start_time)
                ELIGIBILITY_REQUESTS.labels(status='success').inc()
                return result
            except Exception as e:
                ELIGIBILITY_LATENCY.labels(phase=phase).observe(time.time() - start_time)
                ELIGIBILITY_REQUESTS.labels(status='error').inc()
                raise e
        return wrapper
    return decorator

def update_system_metrics():
    """Update system metrics."""
    SYSTEM_MEMORY.set(psutil.virtual_memory().used)
    CPU_USAGE.set(psutil.cpu_percent())

def set_model_info(model_name: str, model_version: str):
    """Update AI model information."""
    AI_MODEL_INFO.info({
        'name': model_name,
        'version': model_version,
        'last_updated': time.strftime('%Y-%m-%d %H:%M:%S')
    }) 