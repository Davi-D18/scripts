{% if cookiecutter.usar_banco_de_dados == "s" %}
from app.extensions import db

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
{% else %}
# Banco de dados não configurado; modelo não implementado.
class News:
    pass
{% endif %}
