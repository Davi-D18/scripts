from typing import List
from .base import BaseConfig

class DRFConfig(BaseConfig):
    def __init__(
        self,
        default_authentication: List[str] = None,
        default_permission: List[str] = None,
        default_pagination: str = None,
        page_size: int = None
    ):
        {%- if cookiecutter.use_authentication == "yes" %}
        # Valores padrão para autenticação e permissões
        self.default_authentication_classes = default_authentication or [
            "rest_framework_simplejwt.authentication.JWTAuthentication"
        ]
        
        self.default_permission_classes = default_permission or [
            "rest_framework.permissions.IsAuthenticated"
        ]
        {%- else %}
        self.default_permission_classes = default_permission or [
            "rest_framework.permissions.AllowAny"
        ]
        {%- endif %}
        
        self.default_pagination_class = default_pagination or \
            "rest_framework.pagination.PageNumberPagination"
        
        self.page_size = page_size or 20