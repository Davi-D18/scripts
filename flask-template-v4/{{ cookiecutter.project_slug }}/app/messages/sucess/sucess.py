from flask import jsonify

class APISuccess:
    """Classe base para todas as mensagens de sucesso da API"""
    status_code = 200
    message = "Operação realizada com sucesso"

    def __init__(self, message=None, data=None):
        self.message = message or self.message
        self.data = data

    def to_response(self):
        """Retorna resposta padronizada em JSON para mensagens de sucesso"""
        response = {
            "message": self.message
        }
        if self.data is not None:
            response["data"] = self.data
        return jsonify(response), self.status_code

# Exemplo de mensagem de sucesso específica
class ResourceCreated(APISuccess):
    status_code = 201
    message = "Recurso criado com sucesso"