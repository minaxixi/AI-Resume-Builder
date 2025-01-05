import logging
import sys

# Logging configuration
logconfig_dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': sys.stdout
        },
    },
    'loggers': {
        '': {  # Root logger
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}

# Gunicorn config
bind = "0.0.0.0:8080"
timeout = 120  # Increase worker timeout to 120 seconds
keepalive = 65  # Keep connections alive for 65 seconds
graceful_timeout = 120  # Grace period for workers to finish serving requests
workers = 2  # Number of worker processes
worker_class = 'sync'  # Use sync workers as they handle long-running tasks better
threads = 1  # Threads per worker
capture_output = True
enable_stdio_inheritance = True
accesslog = '-'  # Log to stdout
errorlog = '-'   # Log to stderr
loglevel = 'debug'
