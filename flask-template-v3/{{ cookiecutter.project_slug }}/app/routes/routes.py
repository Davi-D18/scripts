from flask import Blueprint, jsonify, request
{% if cookiecutter.usar_docs_api == s %}
from flasgger import swag_from
{% endif %}
from app.services import create_news

main = Blueprint('main', __name__)

@main.route('/')
{% if cookiecutter.usar_docs_api == s %}
@swag_from('../../swagger/teste.yml')
{% endif %}
def index():
    return jsonify(message="Tudo Funcionando :)")

@main.route('/news', methods=['POST'])
def create():
    request_data = request.get_json()
    title = request_data.get('title')
    content = request_data.get('content')
    return create_news(title, content)
