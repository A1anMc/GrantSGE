import os
from typing import Dict, Any

class Config:
    """Base configuration."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///grants.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    RATE_LIMIT_DEFAULT = "100 per minute"
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    REDIS_DB = 1

class ProductionConfig(Config):
    """Production configuration."""
    if not os.getenv('SECRET_KEY'):
        raise ValueError("SECRET_KEY must be set in production")
    if not os.getenv('JWT_SECRET_KEY'):
        raise ValueError("JWT_SECRET_KEY must be set in production")
    if not os.getenv('ANTHROPIC_API_KEY'):
        raise ValueError("ANTHROPIC_API_KEY must be set in production")

config: Dict[str, Any] = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 