{% if cookiecutter.usar_banco_de_dados == "s" %}
import os

DATABASE_URI = os.getenv('DATABASE_URL')

if not DATABASE_URI:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'data.db')}"

DATABASE_CONFIG = {
    "DATABASE_URI": DATABASE_URI
}
{% endif %}
