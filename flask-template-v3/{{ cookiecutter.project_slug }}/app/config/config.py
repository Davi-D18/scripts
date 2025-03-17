from app.database.config import DATABASE_CONFIG

class Config:
    """Configuração base usada por todos os ambientes."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    {% if cookiecutter.usar_docs_api == "s" %}
    SWAGGER = {
        'uiversion': 3,
        'specs_route': '/docs/',
        'public': False
    }
    {% endif %}

class DevelopmentConfig(Config):
    """Configurações específicas para o ambiente de desenvolvimento."""
    DEBUG = True
    {% if cookiecutter.usar_banco_de_dados == "s" %}
    SQLALCHEMY_DATABASE_URI = DATABASE_CONFIG["DATABASE_URI"]
    {% endif %}
    {% if cookiecutter.usar_docs_api == "s" %}
    SWAGGER = {
        **Config.SWAGGER,  # Herda as configurações base
        'enabled': True,
        'title': 'API Docs',
        'description': 'Documentação interativa para desenvolvimento',
        'version': '1.0',
        'validatorUrl': None  # Desativa validação externa para performance
    }
    {% endif %}

class ProductionConfig(Config):
    """Configurações específicas para o ambiente de produção."""
    DEBUG = False
    TESTING = False
    {% if cookiecutter.usar_banco_de_dados == "s" %}
    SQLALCHEMY_DATABASE_URI = DATABASE_CONFIG["DATABASE_URI"]
    {% endif %}
    {% if cookiecutter.usar_docs_api == "s" %}
    SWAGGER = {
        **Config.SWAGGER,
        'enabled': False,  # Desativa a UI completamente
        'public': False
    }
    {% endif %}
# Dicionário para mapear os ambientes
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
