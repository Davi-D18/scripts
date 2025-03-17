import os

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
