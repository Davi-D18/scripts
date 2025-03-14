#!/usr/bin/env python3

import os
import subprocess

# Perguntas para o usuário
project_name = input("Digite o nome do seu projeto: ")
use_db = input("Deseja adicionar suporte a banco de dados? (s/n): ").strip().lower() == "s"
use_auth = input("Deseja incluir sistema de autenticação? (s/n): ").strip().lower() == "s"
use_api_docs = input("Deseja adicionar documentação OpenAPI? (s/n): ").strip().lower() == "s"
use_middleware = input("Deseja adicionar middlewares? (s/n): ").strip().lower() == "s"
use_logging = input("Deseja adicionar configuração de logging? (s/n): ").strip().lower() == "s"

if os.path.exists(project_name):
    resp = input(f"⚠️  O diretório '{project_name}' já existe. Sobrescrever? (s/n): ").strip().lower()
    if resp != "s":
        print("Operação cancelada pelo usuário")
        exit()
    import shutil  # Garanta que 'import shutil' esteja no topo do script
    shutil.rmtree(project_name)
    print(f"🗑️  Diretório antigo '{project_name}' removido")

# Criando diretórios baseados nas escolhas do usuário
project_structure = {
    project_name: [
        "app",
        "app/models",
        "app/services",
        "app/routes",
        "tests",
        "tests/api",
        "tests/services",
    ]
}

# Adicionando diretórios extras conforme escolhas
if use_db:
    project_structure[project_name].extend([
        "app/repositories",
        "app/extensions"
    ])

if use_api_docs:
    project_structure[project_name].append("app/docs")

if use_middleware:
    project_structure[project_name].append("app/middlewares")

if use_logging:
    project_structure[project_name].append("app/logging")

# Criar os diretórios
for base, dirs in project_structure.items():
    for d in dirs:
        dir_path = os.path.join(base, d)
        os.makedirs(dir_path, exist_ok=True)

# Criando arquivos essenciais com código funcional
files = {
    f"{project_name}/app/__init__.py": f"""from flask import Flask
from .config import DevelopmentConfig
from .extensions import db{', jwt' if use_auth else ''}{', ma' if use_api_docs else ''}
{'from flask_migrate import Migrate' if use_db else ''}

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    # Inicializar extensões
    db.init_app(app){'''
    Migrate(app, db)''' if use_db else ''}{'''
    jwt.init_app(app)''' if use_auth else ''}{'''
    ma.init_app(app)''' if use_api_docs else ''}

    # Registrar blueprints
    from .routes import news_bp{', auth_bp' if use_auth else ''}
    app.register_blueprint(news_bp){'''
    app.register_blueprint(auth_bp)''' if use_auth else ''}

    # Criar tabelas se não existirem
    with app.app_context():
        db.create_all()

    return app
""",
    
    f"{project_name}/app/config.py": f"""import os

class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-123'){'''
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False''' if use_db else ''}{'''
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-123')''' if use_auth else ''}
""",
    
    f"{project_name}/app/extensions.py": f"""# Centralizador de extensões
from flask_sqlalchemy import SQLAlchemy
{'''
from flask_jwt_extended import JWTManager''' if use_auth else ''}{'''
from flask_marshmallow import Marshmallow''' if use_api_docs else ''}

db = SQLAlchemy(){'''
jwt = JWTManager()''' if use_auth else ''}{'''
ma = Marshmallow()''' if use_api_docs else ''}
""",
    
    f"{project_name}/app/routes/__init__.py": """from .news import news_bp""",
    
    f"{project_name}/app/routes/news.py": """from flask import Blueprint, jsonify
from app.services.news_service import get_all_news

news_bp = Blueprint('news', __name__)

@news_bp.route('/news', methods=['GET'])
def get_news():
    news = get_all_news()
    return jsonify([n.serialize() for n in news])
""",
    
    f"{project_name}/app/models/news.py": f"""from app.extensions import db

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def serialize(self):
        return {{
            'id': self.id,
            'title': self.title,
            'content': self.content
        }}
""",
    
    f"{project_name}/app/services/news_service.py": """from app.models.news import News
from app.extensions import db

def get_all_news():
    try:
        return News.query.all()
    except:
        db.session.rollback()
        return []
""",
}

# Requirements.txt
requirements = ["Flask", "pytest", "python-dotenv"]
if use_db:
    requirements.extend(["Flask-SQLAlchemy", "Flask-Migrate"])
if use_auth:
    requirements.append("Flask-JWT-Extended")
if use_api_docs:
    requirements.extend(["flask-marshmallow", "apispec", "marshmallow-sqlalchemy"])

files[f"{project_name}/requirements.txt"] = "\n".join(requirements)

# Seção do banco de dados
if use_db:
    files.update({
        f"{project_name}/app/extensions/database.py": """from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

def shutdown_session(exception=None):
    db.session.remove()
""",
        f"{project_name}/app/repositories/news_repo.py": """from app.extensions import db
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
"""
    })

# Seção de autenticação
if use_auth:
    files.update({
        f"{project_name}/app/routes/auth.py": """from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    access_token = create_access_token(identity='user_id')
    return jsonify(access_token=access_token)
""",
        f"{project_name}/app/models/user.py": """from app.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
"""
    })

# Arquivo principal de execução
files[f"{project_name}/run.py"] = f"""from app import create_app
{'from app.extensions import db' if use_db else ''}

app = create_app()

{'@app.cli.command("create-db")' if use_db else ''}
{'def create_database():' if use_db else ''}
{'    with app.app_context():' if use_db else ''}
{'        db.create_all()' if use_db else ''}

if __name__ == '__main__':
    app.run(debug=True)
"""

# Middlewares
if use_middleware:
    files[f"{project_name}/app/middlewares/auth_middleware.py"] = """from flask import request, jsonify
from functools import wraps

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token missing!'}), 401
        return f(*args, **kwargs)
    return decorated_function
"""

# Logging
if use_logging:
    files[f"{project_name}/app/logging/log_config.py"] = """import logging
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
"""

# Criar os arquivos
for filepath, content in files.items():
    if content:
        with open(filepath, "w") as f:
            f.write(content)

# Ambiente virtual e instalação de dependências
venv_path = os.path.abspath(os.path.join(project_name, "venv"))
subprocess.run(["python3", "-m", "venv", venv_path], check=True)
print(f"✅ Ambiente virtual criado em {venv_path}")

subprocess.run(
    [os.path.join(venv_path, "bin", "pip"), "install", "-r", os.path.join(project_name, "requirements.txt")],
    check=True
)
print("✅ Dependências instaladas!")

if use_db:
    print("⏳ Configurando banco de dados...")
    try:
        # Definir flask_path corretamente
        flask_path = os.path.join(venv_path, "bin", "flask")
        
        # Verificar e remover migrations existente
        migrations_dir = os.path.join(project_name, "migrations")
        if os.path.exists(migrations_dir):
            import shutil
            shutil.rmtree(migrations_dir)
            print("♻️  Diretório migrations antigo removido")

        # Comandos corrigidos
        commands = [
            [flask_path, "--app", "run.py", "db", "init"],
            [flask_path, "--app", "run.py", "db", "migrate", "-m", "Initial migration"],
            [flask_path, "--app", "run.py", "db", "upgrade"]
        ]
        
        for cmd in commands:
            subprocess.run(cmd, check=True, cwd=project_name)
            
        print("✅ Banco de dados configurado!")
    except Exception as e:
        print(f"❌ Erro crítico: {str(e)}")
        print("Execute manualmente para diagnóstico:")
        print(f"cd {project_name} && source venv/bin/activate")
        print("flask --app run.py db init && flask db migrate && flask db upgrade")

print("\n🎉 Estrutura de projeto criada com sucesso!")
print(f"Para começar a trabalhar, entre no diretório: cd {project_name}")
print(f"Ative o ambiente virtual: source {venv_path}/bin/activate")
