import logging
import logging.config
from pythonjsonlogger import jsonlogger
import os
from datetime import datetime

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['timestamp'] = datetime.utcnow().isoformat()
        log_record['level'] = record.levelname
        log_record['logger'] = record.name

def setup_logging(app):
    """Configure structured logging."""
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                '()': CustomJsonFormatter,
                'format': '%(timestamp)s %(level)s %(name)s %(message)s'
            },
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'json',
                'filename': 'logs/app.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            },
            'error_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'json',
                'filename': 'logs/error.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
                'level': 'ERROR'
            }
        },
        'loggers': {
            '': {  # Root logger
                'handlers': ['console', 'file', 'error_file'],
                'level': log_level,
                'propagate': True
            },
            'werkzeug': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False
            },
            'sqlalchemy.engine': {
                'handlers': ['file'],
                'level': 'WARNING',
                'propagate': False
            }
        }
    }

    # Apply configuration
    logging.config.dictConfig(logging_config)

    # Configure Flask app logging
    app.logger.handlers = []
    for handler in logging.getLogger().handlers:
        app.logger.addHandler(handler) 