from .base import BaseSettings
{% if cookiecutter.use_authentication == "yes" %}
from datetime import timedelta
from core.configs.libs.jwt import JWTConfig
from core.configs.libs.cors import CorsConfig

ACESS_TOKEN_MINUTES = timedelta(minutes=50)
{%- endif %}
CORS_CONFIG = CorsConfig.for_production()

class ProductionSettings(BaseSettings):
    """
    Configurações de produção.
    """
    DATABASE_ALIAS = "production"
    ENVIRONMENT_NAME = "Production"
    DEBUG = False

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

    ALLOW_ALL_ORIGINS = CORS_CONFIG["CORS_ALLOW_ALL_ORIGINS"]
    ALLOWED_HOSTS = CORS_CONFIG["CORS_ALLOWED_HOSTS"]
    CORS_ALLOWED_ORIGINS = CORS_CONFIG["CORS_ALLOWED_ORIGINS"]

    {% if cookiecutter.use_authentication == "yes" %}
    SIMPLE_JWT = JWTConfig(access_token=ACESS_TOKEN_MINUTES).as_dict()
    {%- endif %}
