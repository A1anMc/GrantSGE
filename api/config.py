import os
from typing import Dict, Any
from datetime import timedelta

# JWT Configuration
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///grants.db')

# CORS Configuration
CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')

class Config:
    """Base configuration."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    JWT_SECRET_KEY = JWT_SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = JWT_ACCESS_TOKEN_EXPIRES
    JWT_REFRESH_TOKEN_EXPIRES = JWT_REFRESH_TOKEN_EXPIRES
    RATE_LIMIT_DEFAULT = "100 per minute"
    CORS_ORIGINS = CORS_ORIGINS

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    REDIS_DB = 1

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

config: Dict[str, Any] = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 