from decouple import config

from .base import BaseSettings


class ProductionSettings(BaseSettings):
    """Configurações de produção."""

    DATABASE_ALIAS = "production"
    ENVIRONMENT_NAME = "Production"
    DEBUG = False

    ALLOWED_HOSTS = [
        host.strip()
        for host in config("DJANGO_ALLOWED_HOSTS", "").split(",")
        if host.strip()
    ]
    CSRF_TRUSTED_ORIGINS = [
        origin.strip()
        for origin in config("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
        if origin.strip()
    ]

    # Segurança
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

    STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
        },
    }

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "level": "ERROR",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
            "db": {
                "level": "WARNING",
                "class": "django_db_logger.db_log_handler.DatabaseLogHandler",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console", "db"],
                "level": "WARNING",
                "propagate": True,
            },
            "django_db_logger": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }
