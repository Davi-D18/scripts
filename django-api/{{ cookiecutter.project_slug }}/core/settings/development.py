"""
Configurações de desenvolvimento.
"""

from .base import *  # noqa: F403
from datetime import timedelta

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
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}
{%- endif %}

ALLOWED_HOSTS = ['*'] # Permitir todos os hosts em desenvolvimento
