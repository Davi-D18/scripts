from flask import Flask
from .config import DevelopmentConfig
from .extensions import db{% if cookiecutter.use_auth == "y" %}, jwt{% endif %}{% if cookiecutter.use_api_docs == "y" %}, ma{% endif %}

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    
    {% if cookiecutter.use_db == "y" %}
    # Inicializar extensões relacionadas ao banco de dados
    db.init_app(app)
    from flask_migrate import Migrate
    Migrate(app, db)
    {% endif %}
    
    {% if cookiecutter.use_auth == "y" %}
    jwt.init_app(app)
    {% endif %}
    
    {% if cookiecutter.use_api_docs == "y" %}
    ma.init_app(app)
    {% endif %}
    
    # Registrar blueprints
    from .routes import news_bp{% if cookiecutter.use_auth == "y" %}, auth_bp{% endif %}
    app.register_blueprint(news_bp)
    {% if cookiecutter.use_auth == "y" %}
    app.register_blueprint(auth_bp)
    {% endif %}
    
    {% if cookiecutter.use_db == "y" %}
    # Criar tabelas se não existirem
    with app.app_context():
        db.create_all()
    {% endif %}
    
    return app
