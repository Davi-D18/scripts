import os

ENV_ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")
ENV_ALLOWED_ORIGINS = os.getenv("DJANGO_CORS_ALLOWED_ORIGINS", "").split(",")

class CorsConfig:
    @staticmethod
    def for_development() -> dict:
        """Configuração padrão para ambiente de desenvolvimento"""
        return {
            "CORS_ALLOW_ALL_ORIGINS": True,
        }

    @staticmethod
    def for_production() -> dict:
        """Configuração padrão para ambiente de produção"""
        return {
            "CORS_ALLOW_ALL_ORIGINS": False,
            "CORS_ALLOWED_ORIGINS": ENV_ALLOWED_ORIGINS,
            "CORS_ALLOW_CREDENTIALS": True,
            "CORS_ALLOWED_HOSTS": ENV_ALLOWED_HOSTS
        }