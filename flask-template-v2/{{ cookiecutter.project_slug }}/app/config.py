from .database.config import DATABASE_CONFIG

DEBUG = True
{% if cookiecutter.usar_banco_de_dados == "s" %}
# Configuração do banco de dados
SQLALCHEMY_DATABASE_URI = DATABASE_CONFIG["DATABASE_URI"]
SQLALCHEMY_TRACK_MODIFICATIONS = False
{% endif %}
