from typing import Dict, Any
from .base import BaseConfig

class SwaggerConfig(BaseConfig):
    def __init__(
        self,
        *,
        title: str = "API Documentation",
        version: str = "v1",
        description: str = "API documentation",
        contact_name: str = None,
        contact_email: str = None,
        contact_url: str = None,
        license_name: str = None,
        license_url: str = None,
        public: bool = True,
        authentication_classes: list = [],
        permission_classes: list = [],
    ):
        self.title = title
        self.version = version
        self.description = description
        self.contact_name = contact_name
        self.contact_email = contact_email
        self.contact_url = contact_url
        self.license_name = license_name
        self.license_url = license_url
        self.public = public
        self.authentication_classes = authentication_classes
        self.permission_classes = permission_classes
        self.serve_include_schema = False  # Corrigido para snake_case
        self.components_split_request = True  # Adicionado para melhor compatibilidade

    def as_dict(self) -> Dict[str, Any]:
        config = {
            'TITLE': self.title,
            'VERSION': self.version,
            'DESCRIPTION': self.description,
            'SERVE_INCLUDE_SCHEMA': self.serve_include_schema,
            'COMPONENT_SPLIT_REQUEST': self.components_split_request,
            'SCHEMA_PATH_PREFIX': '/api/',
        }
        
        # Adiciona informações de contato se existirem
        contact = self._create_contact()
        if contact:
            config['CONTACT'] = contact
        
        # Adiciona informações de licença se existirem
        license_info = self._create_license()
        if license_info:
            config['LICENSE'] = license_info
        
        return config

    def _create_contact(self) -> dict:
        if any([self.contact_name, self.contact_email, self.contact_url]):
            return {
                "name": self.contact_name,
                "email": self.contact_email,
                "url": self.contact_url
            }
        return None

    def _create_license(self) -> dict:
        if any([self.license_name, self.license_url]):
            return {
                "name": self.license_name,
                "url": self.license_url
            }
        return None