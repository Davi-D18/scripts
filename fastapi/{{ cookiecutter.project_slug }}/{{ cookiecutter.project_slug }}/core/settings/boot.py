from enum import Enum

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Environment(str, Enum):
    """Enum com os ambientes disponíveis da aplicação."""

    DEVELOPMENT = 'development'
    PRODUCTION = 'production'


class BootSettings(BaseSettings):
    """
    Configurações de inicialização para determinar o ambiente da aplicação.
    """

    model_config = ConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    ENVIRONMENT: Environment
