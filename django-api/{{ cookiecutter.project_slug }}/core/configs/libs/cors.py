from decouple import config

from .base import BaseConfig


class CorsConfig(BaseConfig):
    def __init__(
        self,
        allow_all_origins=False,
        allowed_origins=None,
        allowed_hosts=None,
        allow_credentials=True,
    ):
        self.cors_allow_all_origins = allow_all_origins
        self.cors_allowed_origins = allowed_origins or self._parse_list(
            config("DJANGO_CORS_ALLOWED_ORIGINS", "")
        )
        self.cors_allow_credentials = allow_credentials
        self.allowed_hosts = allowed_hosts or self._parse_list(
            config("DJANGO_ALLOWED_HOSTS", "")
        )

    @staticmethod
    def _parse_list(value):
        return [item.strip() for item in value.split(",") if item.strip()]

    @classmethod
    def for_development(cls):
        return cls(allow_all_origins=True)

    @classmethod
    def for_production(cls):
        return cls(allow_all_origins=False)
