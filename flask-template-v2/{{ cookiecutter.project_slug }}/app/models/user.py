{% if cookiecutter.usar_sistema_de_login == "s" %}
from app.extensions.database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(200))
{% else %}
# Sistema de login não configurado.
class User:
    pass
{% endif %}
