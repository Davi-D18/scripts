from typing import List

from pydantic_settings import SettingsConfigDict

from .base import BaseSettings


class ProductionSettings(BaseSettings):
    """Configurações específicas para o ambiente de produção."""
    model_config = SettingsConfigDict(
        env_prefix='PROD_',
    )

    DEBUG: bool = False

    # CORS Settings
    CORS_ORIGINS: List[str]
    CORS_METHODS: List[str]
    CORS_HEADERS: List[str]
    ALLOWED_HOSTS: List[str]
