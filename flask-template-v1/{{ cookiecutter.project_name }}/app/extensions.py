from flask_sqlalchemy import SQLAlchemy
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
