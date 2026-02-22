from typing import List

from .base import BaseSettings


class ProductionSettings(BaseSettings):
    """Configurações específicas para o ambiente de produção."""
    DEBUG: bool = False

    # CORS Settings
    CORS_ORIGINS: List[str]
    CORS_METHODS: List[str]
    CORS_HEADERS: List[str]
    ALLOWED_HOSTS: List[str]
