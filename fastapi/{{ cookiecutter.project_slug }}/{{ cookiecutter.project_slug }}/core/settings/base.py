from pydantic_settings import BaseSettings as Bs
from pydantic_settings import SettingsConfigDict


class BaseSettings(Bs):
    """
    Configurações base da aplicação com variáveis
    comuns a todos os ambientes.
    """

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    DEBUG: bool = True
    DATABASE_URL: str
