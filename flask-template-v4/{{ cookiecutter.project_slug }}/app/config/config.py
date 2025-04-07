from app.database.config import DATABASE_CONFIG
import os

class Config:
    """Configuração base usada por todos os ambientes."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_MAX_BYTES = int(os.getenv("LOG_MAX_BYTES", 10000))
    LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", 3))
    LOG_FILE = os.getenv("LOG_FILE", "errors.log")
    {%- if cookiecutter.usar_docs_api == "s" %}
    SWAGGER = {
        'uiversion': 3,
        'specs_route': '/docs/',
        'public': False
    }
    {%- endif %}

class DevelopmentConfig(Config):
    """Configurações específicas para o ambiente de desenvolvimento."""
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    PROPAGATE_EXCEPTIONS = os.getenv("PROPAGATE_EXCEPTIONS", "True").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").lower() == "true"  # Log mais detalhado
    LOG_FILE = None  # Log apenas no console

    SQLALCHEMY_DATABASE_URI = DATABASE_CONFIG["DATABASE_URI"]
    {%- if cookiecutter.usar_docs_api == "s" %}
    SWAGGER = {
        **Config.SWAGGER,  # Herda as configurações base
        'title': 'API Docs',
        'description': 'Documentação interativa para desenvolvimento',
        'version': '1.0',
        'validatorUrl': None,  # Desativa validação externa para performance,
        'enabled': os.getenv("ENABLE_SWAGGER", "True").lower() == "true"
    }
    {%- endif %}

class ProductionConfig(Config):
    """Configurações específicas para o ambiente de produção."""
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    TESTING = os.getenv("TESTING", "False").lower() == "true"
    PROPAGATE_EXCEPTIONS = os.getenv("PROPAGATE_EXCEPTIONS", "False").lower() == "true"

    # Configurações de logging para produção
    LOG_LEVEL = os.getenv("LOG_LEVEL", "ERROR").lower() == "true"
    LOG_FILE = "errors.log"

    SQLALCHEMY_DATABASE_URI = DATABASE_CONFIG["DATABASE_URI"]
    {%- if cookiecutter.usar_docs_api == "s" %}
    SWAGGER = {
        **Config.SWAGGER,
        'enabled': os.getenv("ENABLE_SWAGGER", "False").lower() == "true",
        'public': False
    }
    {%- endif %}

# Dicionário para mapear os ambientes
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}