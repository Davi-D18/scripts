from flask import Blueprint, jsonify, request
{% if cookiecutter.usar_flask_restful == "s" %}
from flask_restful import Api, Resource
{% endif %}
{% if cookiecutter.usar_docs_api == "s" %}
from flasgger import swag_from
{% endif %}
{% if cookiecutter.usar_serializacao == "s" %}
from marshmallow import ValidationError
from app.schemas.news_schema import NewsSchema
{% endif %}
from app.services import create_news, lista_news
{% if cookiecutter.usar_serializacao == "s" %}
from app.messages.errors.error import InvalidInputError, InternalServerError
from app.messages.sucess.sucess import ResourceCreated
news_schema = NewsSchema()
{% endif %}
main = Blueprint('main', __name__)
{% if cookiecutter.usar_flask_restful == "s" %}
api = Api(main)
{% endif %}

{% if cookiecutter.usar_flask_restful == "s" %}
class IndexResource(Resource):
    def get(self):
        return jsonify(message="Tudo Funcionando :)")

class NewsResource(Resource):
    def post(self):
        json_data = request.get_json()
        {% if cookiecutter.usar_serializacao == "s" %}
        try:
            data = news_schema.load(json_data)
        except ValidationError as err:
            raise InvalidInputError(
                message="Dados inválidos na requisição",
                details=err.messages
            )
            
        status = create_livros(
            data['title'],
            data['content'],
        )

        match(status):
            case 201:
                return ResourceCreated(
                    message="News criado com sucesso"
                ).to_response()
            case 500:
                return InternalServerError(
                    message="Erro interno do servidor"
                ).to_response()
        
    def get(self):
        dados = lista_news()
        return news_schema.dump(dados, many=True)
        {% else %}
        title = json_data.get('title')
        content = json_data.get('content')
        
        return create_news(title, content)
        
    def get(self):
        return lista_news()
        {% endif %}

api.add_resource(IndexResource, '/')
api.add_resource(NewsResource, '/news')
{% else %}
@main.route('/')
{% if cookiecutter.usar_docs_api == "s" %}
@swag_from('../../swagger/teste.yml')
{% endif %}
def index():
    return jsonify(message="Tudo Funcionando :)")
    
@main.route("/news", methods=['GET'])
def retornar_news():
 {% if cookiecutter.usar_serializacao == "s" %}
    dados = lista_news()
    return news_schema.dump(dados, many=True)
 {% else %}
    return jsonify(lista_news())
 {% endif %}
 
@main.route('/news', methods=['POST'])
def create():
    json_data = request.get_json()
    {% if cookiecutter.usar_serializacao == "s" %}
    try:
        data = news_schema.load(json_data)
    except ValidationError as err:
        raise InvalidInputError(
            message="Validação falhou",
            details=err.messages
        )
        
    status = create_livros(
        data['title'],
        data['content'],
    )

    match(status):
        case 201:
            return ResourceCreated(
                message="News criado com sucesso"
            ).to_response()
        case 500:
            return InternalServerError(
                message="Erro interno do servidor"
            ).to_response()
    {% else %}
    title = json_data.get('title')
    content = json_data.get('content')

    if not title or not content:
        raise InvalidInputError(
            message="Dados incompletos",
            details={"missing": [f for f in ['title', 'content'] if not json_data.get(f)]}
        )
        
    return create_news(title, content)
    {% endif %}
{% endif %}
