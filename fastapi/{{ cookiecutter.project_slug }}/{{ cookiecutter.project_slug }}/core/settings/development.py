from pydantic_settings import SettingsConfigDict

from .base import BaseSettings


class DevelopmentSettings(BaseSettings):
    """Configurações específicas para o ambiente de desenvolvimento."""
    model_config = SettingsConfigDict(
        env_prefix='DEV_',
    )
