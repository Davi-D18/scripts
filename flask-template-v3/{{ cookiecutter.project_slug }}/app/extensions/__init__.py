{% if cookiecutter.usar_banco_de_dados == "s" %}
from .extensions import db, migrate

__all__ = ["db", "migrate"]
{% endif %}
