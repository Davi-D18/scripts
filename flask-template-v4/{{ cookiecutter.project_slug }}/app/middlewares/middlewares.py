{% if cookiecutter.usar_middlewares == "s" %}
from flask import request, g
import time
import uuid

def middlewares(app):

    @app.before_request
    def before():
        """Executado antes de cada requisição"""
        app.logger.info(f"Recebendo requisição: {request.method} {request.path}")
        
        # Inicia um timer para medir a duração da requisição
        g.start_time = time.time()
        
        # Gera um ID único para a requisição (caso não exista no cabeçalho)
        g.request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))

    @app.after_request
    def after(response):
        """Executado após o processamento da requisição"""
        duration = time.time() - g.start_time
        app.logger.info(f"Requisição processada em {duration:.3f} segundos")
        
        # Adiciona o ID da requisição no cabeçalho da resposta
        response.headers['X-Request-ID'] = g.request_id

        return response

    @app.teardown_request
    def teardown(error=None):
        """Executado no final da requisição, mesmo em caso de erro"""
        if error:
            app.logger.error(f"Erro na requisição: {error}")
{% endif %}
