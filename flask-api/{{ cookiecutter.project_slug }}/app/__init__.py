import os
from flask import Flask

{%- if cookiecutter.usar_docs_api == "s" %}
from flasgger import Swagger
{%- endif %}

# Rotas
# from .routes.produtos_routes import produtos_bp

from .extensions import init_extensions

{%- if cookiecutter.usar_middlewares == "s" %}
from .middlewares.middlewares import middlewares
{%- endif %}
from dotenv import load_dotenv

from .commands.db_commands import register as register_db_commands
from .commands.dev_commands import register as register_dev_commands

from .messages.errors.handlers import configure_error_handlers
from .logs.logger import configure_logging

def create_app():
    app = Flask(__name__)
    load_dotenv()
    
    from .config.config import config
    env = os.getenv('FLASK_ENV', 'development')
    configure_error_handlers(app)
    app.config.from_object(config[env])
    configure_logging(app)
    
    {%- if cookiecutter.usar_docs_api == "s" %}
    # Inicializa o Flasgger APENAS se estiver habilitado
    if app.config.get('SWAGGER', {}).get('enabled', False):
        Swagger(app, template=app.config['SWAGGER'])
    {%- endif %}
    
    init_extensions(app)

    {%- if cookiecutter.usar_middlewares == "s" %}
    middlewares(app)
    {%- endif %}
    
    # Registro das rotas
    # app.register_blueprint(variavel_bp)

    # registra os comandos CLI
    register_db_commands(app)
    register_dev_commands(app)
    
    return app