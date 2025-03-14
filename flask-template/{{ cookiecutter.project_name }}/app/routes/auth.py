{% if cookiecutter.use_auth == "y" %}
from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    access_token = create_access_token(identity='user_id')
    return jsonify(access_token=access_token)
{% endif %}
