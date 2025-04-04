{% if cookiecutter.usar_banco_de_dados == "s" %}
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
{% endif %}
