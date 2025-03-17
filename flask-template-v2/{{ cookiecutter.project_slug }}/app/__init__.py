from flask import Flask
{% if cookiecutter.usar_banco_de_dados == "s" %}
from .extensions import db
{% endif %}

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')
    
    {% if cookiecutter.usar_banco_de_dados == "s" %}
    db.init_app(app)
    {% endif %}
    
    # Registro das rotas
    from .routes.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
