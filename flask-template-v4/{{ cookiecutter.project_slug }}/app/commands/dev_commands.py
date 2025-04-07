# app/commands/dev_commands.py
import click
import subprocess
import os
from flask.cli import with_appcontext

def register(app):
    @app.cli.group('dev', help='Comandos relacionados ao desenvolvimento.')
    def dev():
        pass

    @dev.command('run')
    @click.option('--port', default=5000, help='Porta para rodar o servidor.')
    def run(port):
        """Roda a aplicação Flask."""
        cmd = ['flask', 'run', '--port', str(port)]
        cmd.append('--reload')
        
        subprocess.run(cmd, check=True)

    @dev.command('lint')
    def lint():
        """Executa o linter (flake8)."""
        subprocess.run(['flake8', 'app'], check=True)

    @dev.command('format')
    def fmt():
        """Formata o código (black)."""
        subprocess.run(['black', 'app'], check=True)

    @dev.command('shell')
    @with_appcontext
    def shell():
        """Abre o shell interativo do Flask."""
        os.execvp('flask', ['flask', 'shell'])

    @dev.command('scaffold')
    @click.argument('resource')
    def scaffold(resource):
        """Gera scaffold básico de CRUD para um novo recurso usando Flask-RESTful e Marshmallow."""
        # Normaliza singular e plural
        name = resource.lower().strip()
        if name.endswith('s'):
            plural = name
            singular = name[:-1]
        else:
            singular = name
            plural = f"{name}s"
        class_name = plural.capitalize()

        # Diretórios
        dirs = {
            'model': 'app/models',
            'repo': 'app/repositories',
            'service': 'app/services',
            'schema': 'app/schemas',
            'route': 'app/routes'
        }
        for d in dirs.values():
            os.makedirs(d, exist_ok=True)

        # Model
        model_path = os.path.join(dirs['model'], f'{plural}.py')
        if not os.path.exists(model_path):
            with open(model_path, 'w') as f:
                f.write(f"""from app.extensions import db

class {class_name}(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # adicione outros campos aqui, ex:
    # title = db.Column(db.String(100))
    # content = db.Column(db.Text)

    {% raw %}
    def to_dict(self):
        return {{col.name: getattr(self, col.name) for col in self.__table__.columns}}
    {% endraw %}

""")
            click.echo(f'Model criado em {model_path}')

        # Repository
        repo_path = os.path.join(dirs['repo'], f'{plural}_repository.py')
        if not os.path.exists(repo_path):
            with open(repo_path, 'w') as f:
                f.write(f"""from app.models.{plural} import {class_name}
from app.extensions import db


def obter_{plural}():
    return {class_name}.query.all()


def inserir_{singular}(**kwargs):
    obj = {class_name}(**kwargs)
    db.session.add(obj)
    db.session.commit()
    return obj
""")
            click.echo(f'Repository criado em {repo_path}')

        # Service
        service_path = os.path.join(dirs['service'], f'{plural}_service.py')
        if not os.path.exists(service_path):
            with open(service_path, 'w') as f:
                f.write(f"""from app.repositories.{plural}_repository import obter_{plural}, inserir_{singular}


def lista_{plural}():
    return obter_{plural}()


def create_{singular}(**kwargs):
    try:
        inserir_{singular}(**kwargs)
        return 201
    except Exception:
        return 500
""")
            click.echo(f'Service criado em {service_path}')

        # Schema
        schema_path = os.path.join(dirs['schema'], f'{singular}_schema.py')
        if not os.path.exists(schema_path):
            with open(schema_path, 'w') as f:
                f.write(f"""from marshmallow import Schema, fields, validate, EXCLUDE

class {class_name[:-1]}Schema(Schema):
    class Meta:
        unknown = EXCLUDE  # Ignora campos não declarados

    id = fields.Int(dump_only=True)  # Aparece apenas na resposta

    # Campos de entrada (validação)
    # title = fields.Str(
    #     required=True,
    #     validate=validate.Length(min=3, max=100, error=\"Título deve ter entre 3 e 100 caracteres\"),
    # )
    # content = fields.Str(
    #     required=True,
    #     validate=validate.Length(min=10, error=\"Conteúdo muito curto (mínimo 10 caracteres)\"),
    # )
""")
            click.echo(f'Schema criado em {schema_path}')

        # Routes usando Flask-RESTful
        route_path = os.path.join(dirs['route'], f'{plural}_routes.py')
        if not os.path.exists(route_path):
            with open(route_path, 'w') as f:
                f.write(f"""from flask import request, Blueprint
from flask_restful import Api, Resource
from marshmallow import ValidationError
from app.schemas.{singular}_schema import {class_name[:-1]}Schema
from app.services.{plural}_service import lista_{plural}, create_{singular}
from app.messages.errors.error import InvalidInputError, InternalServerError
from app.messages.sucess.sucess import ResourceCreated

{plural}_bp = Blueprint('{plural}', __name__)
api = Api({plural}_bp)

{singular.lower()}_schema = {singular.capitalize()}Schema()
{singular.lower()}_schema_many = {singular.capitalize()}Schema(many=True)

class {class_name}Resource(Resource):
    def post(self):
        json_data = request.get_json()
        try:
            data = {singular.lower()}_schema.load(json_data)
        except ValidationError as err:
            raise InvalidInputError(message="Dados inválidos na requisição", details=err.messages)

        status = create_{singular}(**data)
        match status:
            case 201:
                return ResourceCreated(message="{class_name} criado com sucesso").to_response()
            case 500:
                raise InternalServerError(message="Erro interno do servidor")

    def get(self):
        items = lista_{plural}()
        return {singular.lower()}_schema_many.dump(items)

class {class_name}ItemResource(Resource):
    def get(self, id):
        # Ajuste para buscar por ID
        # from app.repositories.{plural}_repository import obter_{singular}_por_id
        # item = obter_{singular}_por_id(id)
        item = None
        return {singular.lower()}_schema.dump(item)

api.add_resource({class_name}Resource, '/{plural}')
api.add_resource({class_name}ItemResource, '/<int:id>')
""")
            click.echo(f'Routes criadas em {route_path}')

        click.echo('\nPronto! Registre o blueprint em app/__init__.py:')
        click.echo(f"app.register_blueprint({plural}_bp)")
