from .base import BaseSettings


class DevelopmentSettings(BaseSettings):
    """Configurações de desenvolvimento."""

    DATABASE_ALIAS = "development"
    ENVIRONMENT_NAME = "Development"
    DEBUG = True

    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    INSTALLED_APPS = [
        *BaseSettings.INSTALLED_APPS,
        "django_extensions",
        "debug_toolbar",
    ]

    MIDDLEWARE = [
        *BaseSettings.MIDDLEWARE,
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

    INTERNAL_IPS = ["127.0.0.1", "localhost"]
