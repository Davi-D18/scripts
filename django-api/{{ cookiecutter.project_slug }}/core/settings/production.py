"""
Configurações de produção.
"""
import os
from .base import *  # noqa: F403
{% if cookiecutter.use_authentication == "yes" %}
from datetime import timedelta
{%- endif %}


DEBUG = False
{%- if cookiecutter.banco_de_dados != "sqlite3" %}
DATABASES["default"] = DATABASES["production"]
{%- endif %}

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS settings
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'db': {
            'level': 'WARNING',
            'class': 'django_db_logger.db_log_handler.DatabaseLogHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'db'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django_db_logger': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# CORS settings
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',')
CORS_ALLOWED_ORIGINS = os.getenv('DJANGO_CORS_ALLOWED_ORIGINS', '*').split(',')

{% if cookiecutter.use_authentication == "yes" %}
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=20),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "SIGNING_KEY": os.getenv('JWT_SECRET_KEY', SECRET_KEY),
}
{%- endif %}
