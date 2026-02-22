from pydantic import ConfigDict
from pydantic_settings import BaseSettings as Bs


class BaseSettings(Bs):
    """
    Configurações base da aplicação com variáveis
    comuns a todos os ambientes.
    """

    model_config = ConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    DATABASE_URL: str
    DEBUG: bool = True

    SECRET_KEY: str
