class APIError(Exception):
    """Classe base para todos os erros da API"""
    status_code = 500
    message = "Erro interno do servidor"
    
    def __init__(self, message=None, details=None):
        super().__init__()
        self.message = message or self.message
        self.details = details
    
    def to_response(self):
        """Retorna resposta padronizada em JSON"""
        response = {
            "error": self.__class__.__name__,
            "message": self.message
        }
        if self.details:
            response["details"] = self.details
        return response, self.status_code

# Erros específicos
class ItemNotFoundError(APIError):
    status_code = 404
    message = "Recurso não encontrado"

class InvalidInputError(APIError):
    status_code = 400
    message = "Dados de entrada inválidos"

class InternalServerError(APIError):
    status_code = 500
    message = "Erro interno do servidor"