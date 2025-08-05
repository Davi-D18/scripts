"""
Configurações de desenvolvimento.
"""

from .base import *  # noqa: F403
{%- if cookiecutter.use_authentication == "yes" %}
from datetime import timedelta
import os
{%- endif %}


DEBUG = True

DB = DATABASES["default"]  # noqa: F405

# Email - Override to use console backend in development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

{% if cookiecutter.use_documentation == "yes" %}
# Swagger settings
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}
{% endif %}

{%- if cookiecutter.use_authentication == "yes" %}
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "SIGNING_KEY": os.getenv('JWT_SECRET_KEY', SECRET_KEY),
}
{%- endif %}

CORS_ALLOW_ALL_ORIGINS = True

# Development Tools
INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Debug Toolbar
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]