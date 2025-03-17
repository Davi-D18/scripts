import os
from flask import Flask
{% if cookiecutter.usar_docs_api == "s" %}
from flasgger import Swagger
{% endif %}
from .routes.routes import main as main_blueprint

{% if cookiecutter.usar_banco_de_dados == "s" %}
from .extensions import db, migrate
{% endif %}
{% if cookiecutter.usar_middlewares == "s" %}
from .middlewares.middlewares import middlewares
{% endif %}
from .config.config import config

def create_app():
    app = Flask(__name__)
    
    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[env])
    
    {% if cookiecutter.usar_docs_api == "s" %}
    # Inicializa o Flasgger APENAS se estiver habilitado
    if app.config.get('SWAGGER', {}).get('enabled', False):
        Swagger(app, template=app.config['SWAGGER'])
    {% endif %}
    
    {% if cookiecutter.usar_banco_de_dados == "s" %}
    db.init_app(app)
    migrate.init_app(app, db)
    {% endif %}

    {% if cookiecutter.usar_middlewares == "s" %}
    middlewares(app)
    {% endif %}
    
    # Registro das rotas
    app.register_blueprint(main_blueprint)
    
    return app
