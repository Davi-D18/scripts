from flask import Blueprint, jsonify, request
from services import create_news

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return jsonify(message="Hello, Flask with Cookiecutter Template!")

@main.route('/news', methods=['POST'])
def create():
    request_data = request.get_json()
    title = request_data.get('title')
    content = request_data.get('content')
    return create_news(title, content)
