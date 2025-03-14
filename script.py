#!/usr/bin/env python3
import os
import subprocess
import sys
import shutil

def create_file(path, content):
    """Cria o arquivo e seus diretórios, escrevendo o conteúdo."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    base_dir = "cookiecutter-flask-template"
    os.makedirs(base_dir, exist_ok=True)
    
    # 1. Arquivo cookiecutter.json com chaves extras para ações pós-geração
    cookiecutter_json = '''{
  "project_name": "MeuFlaskApp",
  "use_db": "n",
  "use_auth": "n",
  "use_api_docs": "n",
  "use_middleware": "n",
  "use_logging": "n",
  "setup_venv": "y",
  "install_dependencies": "y",
  "run_db_migrations": "n"
}
'''
    create_file(os.path.join(base_dir, "cookiecutter.json"), cookiecutter_json)
    
    # 2. Hooks: post_gen_project.py aprimorado com remoção de diretórios opcionais
    hooks_dir = os.path.join(base_dir, "hooks")
    os.makedirs(hooks_dir, exist_ok=True)
    post_gen_project = '''import os
import shutil
import subprocess
import sys

def remove_empty_dirs(path):
    # Percorre a árvore de diretórios de baixo para cima e remove os vazios
    for dirpath, dirnames, filenames in os.walk(path, topdown=False):
        if not dirnames and not filenames:
            print(f"Removendo diretório vazio: {dirpath}")
            os.rmdir(dirpath)

def remove_dir_if_exists(path, description):
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            print(f"Removendo {description} por opção do usuário.")
        except Exception as e:
            print(f"❌ Erro ao remover {description}: {e}")

def main():
    project_dir = os.getcwd()
    remove_empty_dirs(project_dir)
    
    # Verifica as opções definidas no cookiecutter via variáveis de ambiente
    use_middleware = os.environ.get("cookiecutter_use_middleware", "n").lower() == "y"
    use_logging = os.environ.get("cookiecutter_use_logging", "n").lower() == "y"
    
    # Se o usuário não quiser middlewares, remove a pasta correspondente
    if not use_middleware:
        middleware_dir = os.path.join(project_dir, "app", "middlewares")
        remove_dir_if_exists(middleware_dir, "diretório de middlewares")
    
    # Se o usuário não quiser logging, remove a pasta correspondente
    if not use_logging:
        logging_dir = os.path.join(project_dir, "app", "logging")
        remove_dir_if_exists(logging_dir, "diretório de logging")
    
    # Criação do ambiente virtual
    setup_venv = os.environ.get("cookiecutter_setup_venv", "y").lower() == "y"
    if setup_venv:
        print("Criando ambiente virtual...")
        venv_path = os.path.join(project_dir, "venv")
        try:
            subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
            print(f"✅ Ambiente virtual criado em {venv_path}")
        except Exception as e:
            print(f"❌ Erro ao criar ambiente virtual: {e}")
    
    # Instalação das dependências
    install_deps = os.environ.get("cookiecutter_install_dependencies", "y").lower() == "y"
    if install_deps:
        print("Instalando dependências...")
        pip_path = os.path.join(project_dir, "venv", "bin", "pip") if os.path.exists(os.path.join(project_dir, "venv", "bin", "pip")) else "pip"
        requirements_path = os.path.join(project_dir, "requirements.txt")
        try:
            subprocess.run([pip_path, "install", "-r", requirements_path], check=True)
            print("✅ Dependências instaladas!")
        except Exception as e:
            print(f"❌ Erro ao instalar dependências: {e}")
    
    # Configuração do banco de dados (se solicitado)
    run_migrations = os.environ.get("cookiecutter_run_db_migrations", "n").lower() == "y"
    use_db = os.environ.get("cookiecutter_use_db", "n").lower() == "y"
    if use_db and run_migrations:
        print("Configurando banco de dados...")
        flask_path = os.path.join(project_dir, "venv", "bin", "flask") if os.path.exists(os.path.join(project_dir, "venv", "bin", "flask")) else "flask"
        migrations_dir = os.path.join(project_dir, "migrations")
        if os.path.exists(migrations_dir):
            try:
                shutil.rmtree(migrations_dir)
                print("♻️  Diretório migrations antigo removido")
            except Exception as e:
                print(f"❌ Erro ao remover migrations: {e}")
        commands = [
            [flask_path, "--app", "run.py", "db", "init"],
            [flask_path, "--app", "run.py", "db", "migrate", "-m", "Initial migration"],
            [flask_path, "--app", "run.py", "db", "upgrade"]
        ]
        for cmd in commands:
            try:
                subprocess.run(cmd, check=True, cwd=project_dir)
            except Exception as e:
                print(f"❌ Erro ao executar comando: {' '.join(cmd)}. Erro: {e}")
        print("✅ Banco de dados configurado!")
    
    print("\\n🎉 Projeto gerado com sucesso!")
    print("Para começar a trabalhar, entre no diretório do projeto e ative o ambiente virtual, se necessário.")

if __name__ == '__main__':
    main()
'''
    create_file(os.path.join(hooks_dir, "post_gen_project.py"), post_gen_project)
    
    # 3. Diretório do template do projeto: {{ cookiecutter.project_name }}
    project_template_dir = os.path.join(base_dir, "{{ cookiecutter.project_name }}")
    os.makedirs(project_template_dir, exist_ok=True)
    
    # 3.1 Diretório app/ e seus arquivos
    app_dir = os.path.join(project_template_dir, "app")
    os.makedirs(app_dir, exist_ok=True)
    
    # app/__init__.py com condições (Jinja2)
    # Agora, a inicialização do db só ocorre se o banco estiver habilitado.
    init_py = '''from flask import Flask
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
'''
    create_file(os.path.join(app_dir, "__init__.py"), init_py)
    
    # app/config.py
    config_py = '''import os

class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-123')
    {% if cookiecutter.use_db == "y" %}
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    {% endif %}
    {% if cookiecutter.use_auth == "y" %}
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-123')
    {% endif %}
'''
    create_file(os.path.join(app_dir, "config.py"), config_py)
    
    # app/extensions.py
    extensions_py = '''from flask_sqlalchemy import SQLAlchemy
{% if cookiecutter.use_auth == "y" %}
from flask_jwt_extended import JWTManager
{% endif %}
{% if cookiecutter.use_api_docs == "y" %}
from flask_marshmallow import Marshmallow
{% endif %}

db = SQLAlchemy()
{% if cookiecutter.use_auth == "y" %}
jwt = JWTManager()
{% endif %}
{% if cookiecutter.use_api_docs == "y" %}
ma = Marshmallow()
{% endif %}
'''
    create_file(os.path.join(app_dir, "extensions.py"), extensions_py)
    
    # 3.2 Diretório app/routes e seus arquivos
    routes_dir = os.path.join(app_dir, "routes")
    os.makedirs(routes_dir, exist_ok=True)
    
    routes_init = '''from .news import news_bp
{% if cookiecutter.use_auth == "y" %}
from .auth import auth_bp
{% endif %}
'''
    create_file(os.path.join(routes_dir, "__init__.py"), routes_init)
    
    news_py = '''from flask import Blueprint, jsonify
from app.services.news_service import get_all_news

news_bp = Blueprint('news', __name__)

@news_bp.route('/news', methods=['GET'])
def get_news():
    news = get_all_news()
    return jsonify([n.serialize() for n in news])
'''
    create_file(os.path.join(routes_dir, "news.py"), news_py)
    
    auth_py = '''{% if cookiecutter.use_auth == "y" %}
from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    access_token = create_access_token(identity='user_id')
    return jsonify(access_token=access_token)
{% endif %}
'''
    create_file(os.path.join(routes_dir, "auth.py"), auth_py)
    
    # 3.3 Diretório app/models e seus arquivos
    models_dir = os.path.join(app_dir, "models")
    os.makedirs(models_dir, exist_ok=True)
    
    models_news = '''from app.extensions import db

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content
        }
'''
    create_file(os.path.join(models_dir, "news.py"), models_news)
    
    models_user = '''{% if cookiecutter.use_auth == "y" %}
from app.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
{% endif %}
'''
    create_file(os.path.join(models_dir, "user.py"), models_user)
    
    # 3.4 Diretório app/services e seus arquivos
    services_dir = os.path.join(app_dir, "services")
    os.makedirs(services_dir, exist_ok=True)
    
    news_service = '''from app.models.news import News
from app.extensions import db

def get_all_news():
    try:
        return News.query.all()
    except:
        db.session.rollback()
        return []
'''
    create_file(os.path.join(services_dir, "news_service.py"), news_service)
    
    # 3.5 Diretório app/repositories (opcional para use_db)
    repositories_dir = os.path.join(app_dir, "repositories")
    os.makedirs(repositories_dir, exist_ok=True)
    
    news_repo = '''from app.extensions import db
from app.models.news import News

class NewsRepository:
    @staticmethod
    def get_all():
        return News.query.all()
    
    @staticmethod
    def create(news_data):
        news = News(**news_data)
        db.session.add(news)
        db.session.commit()
        return news
'''
    create_file(os.path.join(repositories_dir, "news_repo.py"), news_repo)
    
    # 3.6 Diretório app/extensions/database.py (opcional para use_db)
    extensions_db_dir = os.path.join(app_dir, "extensions")
    os.makedirs(extensions_db_dir, exist_ok=True)
    
    database_py = '''from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

def shutdown_session(exception=None):
    db.session.remove()
'''
    create_file(os.path.join(extensions_db_dir, "database.py"), database_py)
    
    # 3.7 Diretório app/docs (opcional para use_api_docs)
    docs_dir = os.path.join(app_dir, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    create_file(os.path.join(docs_dir, ".gitkeep"), "")
    
    # 3.8 Diretório app/middlewares (opcional para use_middleware)
    middlewares_dir = os.path.join(app_dir, "middlewares")
    os.makedirs(middlewares_dir, exist_ok=True)
    
    auth_middleware = '''from flask import request, jsonify
from functools import wraps

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token missing!'}), 401
        return f(*args, **kwargs)
    return decorated_function
'''
    create_file(os.path.join(middlewares_dir, "auth_middleware.py"), auth_middleware)
    
    # 3.9 Diretório app/logging (opcional para use_logging)
    logging_dir = os.path.join(app_dir, "logging")
    os.makedirs(logging_dir, exist_ok=True)
    
    log_config = '''import logging
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
'''
    create_file(os.path.join(logging_dir, "log_config.py"), log_config)
    
    # 4. Diretório tests/ e seus subdiretórios
    tests_dir = os.path.join(project_template_dir, "tests")
    os.makedirs(tests_dir, exist_ok=True)
    api_tests_dir = os.path.join(tests_dir, "api")
    os.makedirs(api_tests_dir, exist_ok=True)
    create_file(os.path.join(api_tests_dir, ".gitkeep"), "")
    services_tests_dir = os.path.join(tests_dir, "services")
    os.makedirs(services_tests_dir, exist_ok=True)
    create_file(os.path.join(services_tests_dir, ".gitkeep"), "")
    
    # 5. Arquivo run.py
    run_py = '''from app import create_app
{% if cookiecutter.use_db == "y" %}
from app.extensions import db
{% endif %}

app = create_app()

{% if cookiecutter.use_db == "y" %}
@app.cli.command("create-db")
def create_database():
    with app.app_context():
        db.create_all()
{% endif %}

if __name__ == '__main__':
    app.run(debug=True)
'''
    create_file(os.path.join(project_template_dir, "run.py"), run_py)
    
    # 6. Arquivo requirements.txt
    requirements_txt = '''Flask
pytest
python-dotenv
{% if cookiecutter.use_db == "y" %}
Flask-SQLAlchemy
Flask-Migrate
{% endif %}
{% if cookiecutter.use_auth == "y" %}
Flask-JWT-Extended
{% endif %}
{% if cookiecutter.use_api_docs == "y" %}
flask-marshmallow
apispec
marshmallow-sqlalchemy
{% endif %}
'''
    create_file(os.path.join(project_template_dir, "requirements.txt"), requirements_txt)
    
    print("Template do Cookiecutter Flask criado com sucesso em:", base_dir)

if __name__ == '__main__':
    main()

