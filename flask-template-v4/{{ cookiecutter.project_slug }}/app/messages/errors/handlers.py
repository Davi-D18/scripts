from .error import APIError
from flask import jsonify

def configure_error_handlers(app):
    # Handler para erros personalizados
    @app.errorhandler(APIError)
    def handle_api_error(error):
        app.logger.error(f"{error.__class__.__name__}: {error.message}")
        return error.to_response()
    
    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({
            "error": "Recurso não encontrado",
        }), 404
    
    @app.errorhandler(500)
    def handle_server_error(error):
        app.logger.error(f"Erro 500: {str(error)}", exc_info=True)
        return jsonify({
            "error": "Erro interno do servidor",
            "message": "Ocorreu um erro inesperado."
        }), 500
